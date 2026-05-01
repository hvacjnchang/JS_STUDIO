# 檔案名稱：main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import CoolProp.CoolProp as CP

app = FastAPI()

# 解決 CORS 問題
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/calculate_cycle")
def calculate_cycle(ref: str, Te: float, Tc: float, SH: float, SC: float):
    try:
        # CoolProp 計算時需要使用絕對溫度 (K)
        Te_K = Te + 273.15
        Tc_K = Tc + 273.15
        
        # 取得蒸發壓力與冷凝壓力 (Pa) -> 轉換為 MPa
        Pe_Pa = CP.PropsSI('P', 'T', Te_K, 'Q', 1, ref)
        Pc_Pa = CP.PropsSI('P', 'T', Tc_K, 'Q', 0, ref)
        Pe_MPa = Pe_Pa / 1e6
        Pc_MPa = Pc_Pa / 1e6

        # --- 點 1: 壓縮機吸氣 (蒸發壓力, 過熱) ---
        T1_K = Te_K + SH
        H1 = CP.PropsSI('H', 'P', Pe_Pa, 'T', T1_K, ref) / 1000 
        S1 = CP.PropsSI('S', 'P', Pe_Pa, 'T', T1_K, ref) / 1000 

        # --- 點 2: 壓縮機排氣 (冷凝壓力, 等熵壓縮) ---
        S2 = S1
        H2 = CP.PropsSI('H', 'P', Pc_Pa, 'S', S2 * 1000, ref) / 1000
        T2_K = CP.PropsSI('T', 'P', Pc_Pa, 'H', H2 * 1000, ref)

        # --- 點 3: 膨脹閥前液態 (冷凝壓力, 過冷) ---
        T3_K = Tc_K - SC
        H3 = CP.PropsSI('H', 'P', Pc_Pa, 'T', T3_K, ref) / 1000
        S3 = CP.PropsSI('S', 'P', Pc_Pa, 'T', T3_K, ref) / 1000

        # --- 點 4: 蒸發器入口 (蒸發壓力, 等焓膨脹) ---
        H4 = H3
        T4_K = CP.PropsSI('T', 'P', Pe_Pa, 'H', H4 * 1000, ref)
        S4 = CP.PropsSI('S', 'P', Pe_Pa, 'H', H4 * 1000, ref) / 1000

        # ==========================================
        # 新增：使用 CoolProp 計算真實飽和曲線 (Saturation Dome)
        # ==========================================
        T_crit = CP.PropsSI('Tcrit', ref) # 取得該冷媒的臨界溫度
        T_min_prop = CP.PropsSI('Tmin', ref) # 取得最低極限溫度
        
        # 決定曲線繪製的最低溫度 (取 Te 往下 40 度，或冷媒極限溫度，兩者取高)
        T_start = max(T_min_prop, Te_K - 40)
        # 為了避免 CoolProp 在絕對臨界點計算發散，最高溫取臨界溫度減 0.2K
        T_end = T_crit - 0.2 
        
        steps = 50
        dome_T, dome_P, dome_H_liq, dome_H_vap, dome_S_liq, dome_S_vap = [],[], [], [], [],[]
        
        for i in range(steps + 1):
            T_current = T_start + i * (T_end - T_start) / steps
            P_current = CP.PropsSI('P', 'T', T_current, 'Q', 0, ref) / 1e6
            
            # 飽和液體 (Q=0)
            H_l = CP.PropsSI('H', 'T', T_current, 'Q', 0, ref) / 1000
            S_l = CP.PropsSI('S', 'T', T_current, 'Q', 0, ref) / 1000
            # 飽和氣體 (Q=1)
            H_v = CP.PropsSI('H', 'T', T_current, 'Q', 1, ref) / 1000
            S_v = CP.PropsSI('S', 'T', T_current, 'Q', 1, ref) / 1000
            
            dome_T.append(T_current - 273.15) # 轉回攝氏度傳給前端
            dome_P.append(P_current)
            dome_H_liq.append(H_l)
            dome_H_vap.append(H_v)
            dome_S_liq.append(S_l)
            dome_S_vap.append(S_v)

        return {
            "status": "success",
            "states":[
                {"id": 1, "T": T1_K - 273.15, "P": Pe_MPa, "H": H1, "S": S1, "name": "吸氣 (Suction)"},
                {"id": 2, "T": T2_K - 273.15, "P": Pc_MPa, "H": H2, "S": S2, "name": "排氣 (Discharge)"},
                {"id": 3, "T": T3_K - 273.15, "P": Pc_MPa, "H": H3, "S": S3, "name": "液態 (Liquid)"},
                {"id": 4, "T": T4_K - 273.15, "P": Pe_MPa, "H": H4, "S": S4, "name": "氣液混和 (Mixture)"}
            ],
            "dome": {
                "T": dome_T, "P": dome_P, 
                "H_liq": dome_H_liq, "H_vap": dome_H_vap, 
                "S_liq": dome_S_liq, "S_vap": dome_S_vap
            }
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}