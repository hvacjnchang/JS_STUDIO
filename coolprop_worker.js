// 1. 引入 CoolProp 的預設匯出 (這是一個初始化工廠函數)
import loadCoolProp from './coolprop.js';

// 建立一個全域變數來儲存載入後的 CoolProp 實例
let CoolProp;

// 2. 啟動並初始化 WASM 模組
loadCoolProp({
    locateFile: function(path) {
        // 確保精準指向同目錄下的 wasm 檔案
        if (path.endsWith('.wasm')) {
            return './coolprop.wasm'; 
        }
        return path;
    }
}).then(function(instance) {
    // 載入成功！將實例存入變數
    CoolProp = instance;
    console.log("CoolProp Worker: WASM 模組初始化完全成功！");
    
    // 通知主執行緒 (HTML) 解鎖畫面
    self.postMessage({ type: 'READY' });

}).catch(function(error) {
    // 如果發生錯誤，將錯誤顯示在主控台
    console.error("CoolProp 初始化失敗:", error);
});


// 3. 接收來自 HTML 的計算請求
self.onmessage = function(event) {
    const data = event.data;

    if (data.type === 'CALCULATE_CYCLE') {
        try {
            const params = data.params;
            const fluid = params.fluid;
            
            // 注意：這裡改成使用我們剛剛建立的 CoolProp 實例來呼叫 PropsSI
            const P_evap = CoolProp.PropsSI('P', 'T', params.T_evap, 'Q', 1, fluid);
            const P_cond = CoolProp.PropsSI('P', 'T', params.T_cond, 'Q', 0, fluid);
            
            const H_evap_out = CoolProp.PropsSI('H', 'T', params.T_evap, 'Q', 1, fluid);
            const H_cond_in = CoolProp.PropsSI('H', 'T', params.T_cond, 'P', P_cond, fluid);

            const resultPayload = {
                enthalpy: [H_evap_out, H_cond_in], 
                pressure: [P_evap, P_cond]         
            };

            self.postMessage({
                type: 'CALCULATION_SUCCESS',
                id: data.id,
                payload: resultPayload
            });

        } catch (error) {
            self.postMessage({
                type: 'CALCULATION_ERROR',
                id: data.id,
                error: error.message || error
            });
        }
    }
};