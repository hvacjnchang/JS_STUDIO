// ------------------------------------------------------------------
// 1. 設定 WebAssembly Module
// 這裡指定 .wasm 檔案的路徑，並在載入完成後通知主執行緒
// ------------------------------------------------------------------
self.Module = {
    // 確保 Worker 能正確找到 coolprop.wasm 檔案
    locateFile: function(path) {
        if (path.endsWith('.wasm')) {
            return 'coolprop.wasm'; // 如果您的 wasm 在其他路徑，請在此修改
        }
        return path;
    },
    // 當 WASM 編譯並初始化完成後觸發
    onRuntimeInitialized: function() {
        console.log("CoolProp Worker: WASM 模組初始化完成");
        // 通知主執行緒 (hvac_analyzer-pro_standalone.html) 可以開始計算了
        self.postMessage({ type: 'READY' });
    }
};

// ------------------------------------------------------------------
// 2. 引入 CoolProp 的 JavaScript 介面 (Glue Code)
// 這會自動讀取 self.Module 的設定並載入 coolprop.wasm
// ------------------------------------------------------------------
try {
    importScripts('coolprop.js'); 
} catch (e) {
    console.error("CoolProp Worker: 無法載入 coolprop.js", e);
}

// ------------------------------------------------------------------
// 3. 處理來自 HTML (主執行緒) 的計算請求
// ------------------------------------------------------------------
self.onmessage = function(event) {
    const request = event.data;

    // 忽略非計算請求
    if (request.type !== 'CALCULATE') return;

    try {
        let result = null;

        // 根據請求的函數類型執行不同的計算
        // 支援一般冷媒計算 (PropsSI) 與 濕空氣計算 (HAPropsSI)
        if (request.func === 'PropsSI') {
            // PropsSI(OutputName, InputName1, Prop1, InputName2, Prop2, FluidName)
            result = Module.PropsSI(
                request.args[0], // 輸出屬性 (如 'H')
                request.args[1], // 輸入屬性1 (如 'T')
                request.args[2], // 輸入數值1
                request.args[3], // 輸入屬性2 (如 'P')
                request.args[4], // 輸入數值2
                request.args[5]  // 冷媒名稱 (如 'R410A')
            );
        } else if (request.func === 'HAPropsSI') {
            // HAPropsSI(OutputName, InputName1, Prop1, InputName2, Prop2, InputName3, Prop3)
            result = Module.HAPropsSI(
                request.args[0], 
                request.args[1], request.args[2], 
                request.args[3], request.args[4], 
                request.args[5], request.args[6]
            );
        } else {
            throw new Error("不支援的函數類型：" + request.func);
        }

        // 計算成功，回傳結果
        self.postMessage({
            type: 'RESULT',
            id: request.id,
            result: result,
            success: true
        });

    } catch (error) {
        // 捕捉 CoolProp 拋出的異常 (例如超出物理極限或查表失敗)
        self.postMessage({
            type: 'ERROR',
            id: request.id,
            error: error.message || error,
            success: false
        });
    }
};