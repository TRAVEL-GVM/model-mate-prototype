import pandas as pd
import numpy as np
import datetime

start_date = '2006-01-01'

indicadores = {

    "Liquidez geral": [12656203, 12690835, 12693946, 12657849, 12672260, 12649394, 12696767, 12697453, 12693833,
                       12663106,
                       12599318, 12679656, 12664610, 12693105, 12646374, 12735076, 12735076],
    "Autonomia Financeira": [12635300, 12632936, 12648166, 12639218, 12813569, 12674801, 12635761, 12637936, 12666520,
                             12670032, 12682698, 12697703, 12681911, 12732718, 12658172, 12670032, 12635372, 12679539],
    "Financiamentos obtidos (% do passivo)": [12623362, 12608571, 12595207, 12618120, 12721495, 12603749, 12715386],
    "Custo dos financiamentos obtidos": [12666991, 12683953, 12648948, 12692345, 12647100, 12673043, 12656030, 12661701,
                                         12665365, 12660176, 12680707, 12665700, 12733795],
    "Rendibilidade do ativo": [12693376, 12664602, 12732717, 12672706, 12664627, 12646614, 12637937, 12661426, 12635770,
                               12659704, 12639219, 12695818, 12694257, 12651038, 12632937, 12635301, 12687839, 12635373,
                               12684683, 12664627],
    "Rendibilidade bruta dos capitais investidos": [12719770, 12598218, 12626560, 12595740, 12587440, 12621254,
                                                    12720020],
    "Cobertura dos gastos de financiamento": [12655571, 12663003, 12660341, 12661698, 12668002, 12672741, 12675876,
                                              12679513, 12679972,
                                              12695785, 12735072, 12656506, 12669219, 12649291, 12664021, 12659490,
                                              12695206],
    "Financiamentos obtidos em % ativo": [12655617, 12687142, 12695079, 12733796, 12696505, 12673132, 12664773,
                                          12664600, 12657555,
                                          12649992, 12794416, 12656219, 12693139, 12693693, 12683552],
    "Margem EBITDA em % dos rendimentos": [12635663, 12638892, 12635374, 12636858, 12637572, 12634175, 12635302,
                                           12632938,
                                           12633338, 12724101, 12591794, 12639220, 12637536, 12637938, 12633428,
                                           12633255,
                                           12618427, 12635771],
    "Rácio dos financiamentos obtidos sobre EBITDA": [12725322, 12609203, 12630347, 12594217, 12594493, 12613764,
                                                      12713960, 12628663],
    "Rendibilidade dos capitais próprios": [12666653, 12670585, 12635377, 12659421, 12635305, 12632941, 12686588,
                                            12679007, 12694401, 12657331,
                                            12733799, 12651582, 12690659, 12639223, 12673201, 12635774, 12637941,
                                            12682868, 12671634],
    "Margem líquida em % dos rendimentos": [12638896, 12635378, 12635667, 12633547, 12635306, 12632942, 12633342,
                                            12632522,
                                            12639224, 12637540, 12635775, 12637942, 12613393, 12635198, 12596294,
                                            12724588],
    "Free cash flow": [12729956, 12587359, 12587536, 12588555, 12590492, 12590767, 12594581],
    "Caixa e depósitos bancários em % do ativo": [12619844, 12589953, 12621615, 12612082, 12621615, 12589953],
    "Margem bruta em % dos rendimentos": [12615278, 12605684, 12598345, 12712860, 12622978],
    "Gastos de depreciação e de amortização": [12598588, 12616413, 12627440, 12598457, 12590944, 12721424],
    "Depreciação (% rendimentos)": [12628936, 12627801, 12612370, 12616893, 12719235],
    "EBITDA em % do volume de negócios": [12715658, 12593289, 12714136, 12589370, 12713010, 12598383],
    "Pressão financeira (gastos de financiamento)": [12635670, 12638899, 12712861, 12633550, 12635417, 12632945,
                                                     12635309, 12633345, 12635742, 12635381,
                                                     12639227, 12637543, 12635778, 12637945, 12632776, 12627526,
                                                     12599533, 12635634, 12730579]

}

indicadores_ecb = {

    "GDP and expenditure components": {
        "Private final consumption, Portugal, Annual": "https://data.ecb.europa.eu/data/datasets/MNA/MNA.A.N.PT.W0.S1M.S1.D.P31._Z._Z._T.XDC.LR.GY",
        "Private final consumption, Portugal, Quarterly": "https://data.ecb.europa.eu/data/datasets/MNA/MNA.Q.Y.PT.W0.S1M.S1.D.P31._Z._Z._T.XDC.LR.GY",
        "Gross fixed capital formation, Portugal, Annual": "https://data.ecb.europa.eu/data/datasets/MNA/MNA.A.N.PT.W0.S1.S1.D.P51G.N11G._T._Z.XDC.LR.GY",
        "Gross fixed capital formation, Portugal, Quarterly": "https://data.ecb.europa.eu/data/datasets/MNA/MNA.Q.Y.PT.W0.S1.S1.D.P51G.N11G._T._Z.XDC.LR.GY",
        "Government final consumption, Portugal, Quarterly": "https://data.ecb.europa.eu/data/datasets/MNA/MNA.Q.Y.PT.W0.S13.S1.D.P3._Z._Z._T.XDC.LR.GY",
        "Government final consumption, Portugal, Annual": "https://data.ecb.europa.eu/data/datasets/MNA/MNA.A.N.PT.W0.S13.S1.D.P3._Z._Z._T.XDC.LR.GY",
        "Imports of goods and services, Portugal, Quarterly": "https://data.ecb.europa.eu/data/datasets/MNA/MNA.Q.Y.PT.W1.S1.S1.C.P7._Z._Z._Z.XDC.LR.GY",
        "Imports of goods and services, Portugal, Annual": "https://data.ecb.europa.eu/data/datasets/MNA/MNA.A.N.PT.W1.S1.S1.C.P7._Z._Z._Z.XDC.LR.GY",
        "Exports of goods and services, Portugal, Quarterly": "https://data.ecb.europa.eu/data/datasets/MNA/MNA.Q.Y.PT.W1.S1.S1.D.P6._Z._Z._Z.XDC.LR.GY",
        "Exports of goods and services, Portugal, Annual": "https://data.ecb.europa.eu/data/datasets/MNA/MNA.A.N.PT.W1.S1.S1.D.P6._Z._Z._Z.XDC.LR.GY",
        "Gross domestic product at market prices, Portugal, Quarterly": "https://data.ecb.europa.eu/data/datasets/MNA/MNA.Q.Y.PT.W2.S1.S1.B.B1GQ._Z._Z._Z.XDC.LR.GY",
        "Gross domestic product at market prices, Portugal, Annual": "https://data.ecb.europa.eu/data/datasets/MNA/MNA.A.N.PT.W2.S1.S1.B.B1GQ._Z._Z._Z.XDC_R_B1GQ.Y.GOY",
    },

    "Corporations": {
        "Net value added of Non financial corporations (growth rate), Portugal, Quarterly": "https://data.ecb.europa.eu/data/datasets/QSA/QSA.Q.N.PT.W0.S11.S1._Z.B.B1N._Z._Z._Z.XDC._T.S.V.G4._T",
        "Net value added of Non financial corporations (growth rate), Portugal, Annual": "https://data.ecb.europa.eu/data/datasets/QSA/QSA.A.N.PT.W0.S11.S1._Z.B.B1N._Z._Z._Z.XDC._T.S.V.GY._T",
        "Gross entrepreneurial income of Non financial corporations as a ratio of gross value added, Portugal, Quarterly": "https://data.ecb.europa.eu/data/datasets/QSA/QSA.Q.N.PT.W0.S11.S1._Z.B.B4G._Z._Z._Z.XDC_R_B1G_CY._T.S.V.C4._T",
        "Gross entrepreneurial income of Non financial corporations, Portugal, Annual": "https://data.ecb.europa.eu/data/datasets/QSA/QSA.A.N.PT.W0.S11.S1._Z.B.B4G._Z._Z._Z.XDC_R_B1G._T.S.V.N._T",
        "Debt securities and loans of Non financial corporations as a ratio of GDP, Portugal, Quarterly": "https://data.ecb.europa.eu/data/datasets/QSA/QSA.Q.N.PT.W0.S11.S1.C.L.LE.F3T4.T._Z.XDC_R_B1GQ_CY._T.S.V.N._T",
        "Debt securities and loans of Non financial corporations as a ratio of GDP, Portugal, Annual": "https://data.ecb.europa.eu/data/datasets/QSA/QSA.A.N.PT.W0.S11.S1.C.L.LE.F3T4.T._Z.XDC_R_B1GQ_CY._T.S.V.N._T",
        "Debt of Non financial corporations as a ratio of total financial liabilities, Portugal, Quarterly": "https://data.ecb.europa.eu/data/datasets/QSA/QSA.Q.N.PT.W0.S11.S1.N.L.LE.FPT.T._Z.XDC_R_F._T.S.V.N._T",
        "Debt of Non financial corporations as a ratio of total financial liabilities, Portugal, Annual": "https://data.ecb.europa.eu/data/datasets/QSA/QSA.A.N.PT.W0.S11.S1.N.L.LE.FPT.T._Z.XDC_R_F._T.S.V.N._T",
        "Total financial assets of Non financial corporations (growth rate), Portugal, Quarterly": "https://data.ecb.europa.eu/data/datasets/QSA/QSA.Q.N.PT.W0.S11.S1.N.A.F.F._Z._Z.XDC._T.S.V.F4._T",
        "Total financial assets of Non financial corporations as a ratio of total financial assets, Portugal, Annual": "https://data.ecb.europa.eu/data/datasets/QSA/QSA.A.N.PT.W0.S11.S1.N.A.F.F._Z._Z.XDC._T.S.V.FY._T",
        "Total financial liabilities of Non financial corporations (growth rate), Portugal, Quarterly": "https://data.ecb.europa.eu/data/datasets/QSA/QSA.Q.N.PT.W0.S11.S1.N.L.F.F._Z._Z.XDC._T.S.V.F4._T",
        "Total financial liabilities of Non financial corporations as a ratio of total financial assets, Portugal, Annual": "https://data.ecb.europa.eu/data/datasets/QSA/QSA.A.N.PT.W0.S11.S1.N.L.F.F._Z._Z.XDC._T.S.V.FY._T",
        "Gross fixed capital formation of Non financial corporations as a ratio of gross value added, Portugal, Quarterly": "https://data.ecb.europa.eu/data/datasets/QSA/QSA.Q.N.PT.W0.S11.S1.N.D.P51G._Z._Z._Z.XDC_R_B1G_CY._T.S.V.C4._T",
        "Gross fixed capital formation of Non financial corporations as a ratio of gross value added, Portugal, Annual": "https://data.ecb.europa.eu/data/datasets/QSA/QSA.A.N.PT.W0.S11.S1.N.D.P51G._Z._Z._Z.XDC_R_B1G_CY._T.S.V.N._T"
    },

    "Households": {
        "Loans granted to households as a ratio of gross disposable income, Portugal, Quarterly": "https://data.ecb.europa.eu/data/datasets/QSA/QSA.Q.N.PT.W0.S1M.S1.N.L.LE.F4.T._Z.XDC_R_B6G_CY._T.S.V.N._T",
        "Loans granted to households as a ratio of gross disposable income, Portugal, Annual": "https://data.ecb.europa.eu/data/datasets/QSA/QSA.A.N.PT.W0.S1M.S1.N.L.LE.F4.T._Z.XDC_R_B6G_CY._T.S.V.N._T",
        "Gross saving of households as a ratio of adjusted gross disposable income, Portugal, Quarterly": "https://data.ecb.europa.eu/data/datasets/QSA/QSA.Q.N.PT.W0.S1M.S1._Z.B.B8G._Z._Z._Z.XDC_R_B6GA_CY._T.S.V.C4._T",
        "Gross saving of households as a ratio of adjusted gross disposable income, Portugal, Annual": "https://data.ecb.europa.eu/data/datasets/QSA/QSA.A.N.PT.W0.S1M.S1._Z.B.B8G._Z._Z._Z.XDC_R_B6GA_CY._T.S.V.N._T",
        "Gross disposable income of households (growth rate), Portugal, Quarterly": "https://data.ecb.europa.eu/data/datasets/QSA/QSA.Q.N.PT.W0.S1M.S1._Z.B.B6G._Z._Z._Z.XDC._T.S.V.G4._T",
        "Gross disposable income of households (growth rate), Portugal, Annual": "https://data.ecb.europa.eu/data/datasets/QSA/QSA.A.N.PT.W0.S1M.S1._Z.B.B6G._Z._Z._Z.XDC._T.S.V.GY._T",
        "Total financial assets of households (growth rate), Portugal, Quarterly": "https://data.ecb.europa.eu/data/datasets/QSA/QSA.Q.N.PT.W0.S1M.S1.N.A.F.F._Z._Z.XDC._T.S.V.F4._T",
        "Total financial assets of households as a ratio of total financial assets, Portugal, Annual": "https://data.ecb.europa.eu/data/datasets/QSA/QSA.A.N.PT.W0.S1M.S1.N.A.F.F._Z._Z.XDC._T.S.V.FY._T",
        "Loans granted to households (growth rate), Portugal, Quarterly": "https://data.ecb.europa.eu/data/datasets/QSA/QSA.Q.N.PT.W0.S1M.S1.N.L.F.F4.T._Z.XDC._T.S.V.F4._T",
        "Loans granted to households as a ratio of total financial assets, Portugal, Annual": "https://data.ecb.europa.eu/data/datasets/QSA/QSA.A.N.PT.W0.S1M.S1.N.L.F.F4.T._Z.XDC._T.S.V.FY._T",
        "Gross fixed capital formation of households as a ratio of adjusted gross disposable income, Portugal, Quarterly": "https://data.ecb.europa.eu/data/datasets/QSA/QSA.Q.N.PT.W0.S1M.S1.N.D.P51G._Z._Z._Z.XDC_R_B6GA_CY._T.S.V.C4._T",
        "Gross fixed capital formation of households as a ratio of adjusted gross disposable income, Portugal, Annual": "https://data.ecb.europa.eu/data/datasets/QSA/QSA.A.N.PT.W0.S1M.S1.N.D.P51G._Z._Z._Z.XDC_R_B6GA_CY._T.S.V.N._T",
        "Final consumption expenditure of households (growth rate), Portugal, Quarterly": "https://data.ecb.europa.eu/data/datasets/QSA/QSA.Q.N.PT.W0.S1M.S1.N.D.P3._Z._Z._Z.XDC._T.S.V.G4._T",
        "Final consumption expenditure of households (growth rate), Portugal, Annual": "https://data.ecb.europa.eu/data/datasets/QSA/QSA.A.N.PT.W0.S1M.S1.N.D.P3._Z._Z._Z.XDC._T.S.V.GY._T"
    },

    "Government finance statistics": {
        "Government deficit(-) or surplus(+) (as % of GDP), Portugal, Quarterly": "https://data.ecb.europa.eu/data/datasets/GFS/GFS.Q.N.PT.W0.S13.S1._Z.B.B9._Z._Z._Z.XDC_R_B1GQ_CY._Z.S.V.CY._T",
        "Government deficit(-) or surplus(+) (as % of GDP), Portugal, Annual": "https://data.ecb.europa.eu/data/datasets/GFS/GFS.A.N.PT.W0.S13.S1._Z.B.B9._Z._Z._Z.XDC_R_B1GQ._Z.S.V.N._T",
        "Government primary deficit(-) or surplus(+) (as % of GDP), Portugal, Quarterly": "https://data.ecb.europa.eu/data/datasets/GFS/GFS.Q.N.PT.W0.S13.S1._Z.B.B9P._Z._Z._Z.XDC_R_B1GQ_CY._Z.S.V.CY._T",
        "Government primary deficit(-) or surplus(+) (as % of GDP), Portugal, Annual": "https://data.ecb.europa.eu/data/datasets/GFS/GFS.A.N.PT.W0.S13.S1._Z.B.B9P._Z._Z._Z.XDC_R_B1GQ._Z.S.V.N._T",
        "Government debt (consolidated) (as % of GDP), Portugal, Quarterly": "https://data.ecb.europa.eu/data/datasets/GFS/GFS.Q.N.PT.W0.S13.S1.C.L.LE.GD.T._Z.XDC_R_B1GQ_CY._T.F.V.N._T",
        "Government debt (consolidated) (as % of GDP), Portugal, Annual": "https://data.ecb.europa.eu/data/datasets/GFS/GFS.A.N.PT.W0.S13.S1.C.L.LE.GD.T._Z.XDC_R_B1GQ._T.F.V.N._T"
    },

    "Labour market indicators": {
        "Total employment, Euro area 20 (fixed composition) as of 1 January 2023, Quarterly": "https://data.ecb.europa.eu/data/datasets/MNA/MNA.Q.N.I9.W2.S1.S1._Z.EMP._Z._T._Z.PS._Z.GY",
        "Unemployment rate, Portugal, Monthly": "https://data.ecb.europa.eu/data/datasets/LFSI/LFSI.M.PT.S.UNEHRT.TOTAL0.15_74.T",
        "Labour Productivity (per persons), Portugal, Quarterly": "https://data.ecb.europa.eu/data/datasets/MNA/MNA.Q.S.PT.W0.S1.S1._Z.LPR_PS._Z._T._Z.XDC.LR.GY",
        "Gross fixed capital formation, Portugal, Annual": "https://data.ecb.europa.eu/data/datasets/MNA/MNA.A.N.PT.W0.S1.S1.D.P51G.N11G._T._Z.XDC.LR.GY",
    }

}


# nb default colors for plots and excel
default_color1 = '#179297'
default_color2 = '#BFCE28'

sidebar_indicators = ("Principal Components Analysis", "Correlation Matrix", "Plots")

dashboard_main_title = "TRAVEL - Statistics Dashboard"

path_bonds = 'C:/Users/Admin/Desktop/app_stats/assets'

travel_logo_url = "https://raw.githubusercontent.com/ricardoandreom/Webscrape/refs/heads/main/travel_logo.webp"


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Connection': 'keep-alive',
}


inflation_str = """
**The Consumer Price Index (CPI)** measures inflation in Portugal based on a set of goods and services representative of the expenditure of resident households. 
The reference year of these time series is 2012.
"""

md_botao_cme = """
    <style>
        .center-button {
            display: flex;
            justify-content: center;
        }
    </style>
    <div class="center-button">
        <a href="https://www.cmegroup.com/markets/interest-rates/cme-fedwatch-tool.html" target="_blank">
            <button>Click to open the CME FedWatch Tool</button>
        </a>
    </div>
"""



container_style_html = """
    <style>
        .gpt-container {
            background-color: #ffffff;
            border-radius: 10px;
            padding: 25px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }
        .gpt-button {
            background: linear-gradient(135deg, #6e8efb, #a777e3);
            color: white;
            border: none;
            padding: 12px 24px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 10px 0;
            cursor: pointer;
            border-radius: 25px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .gpt-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 8px rgba(0,0,0,0.15);
            background: linear-gradient(135deg, #5e7cea, #9d68e1);
        }
        .gpt-textarea {
            border-radius: 10px;
            border: 2px solid #e0e0e0;
            padding: 15px;
            font-size: 16px;
        }
        .gpt-toggle {
            margin: 15px 0;
        }
        .gpt-response {
            background-color: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            margin-top: 20px;
            border-left: 5px solid #6e8efb;
        }
    </style>"""



button_css = """
<style>
    /* Estilo para o botão verde */
    div.stButton > button:first-child {
        background-color: #179297 !important;
        color: white !important;
        border: 1px solid #179297 !important;
    }
    
    div.stButton > button:hover {
        background-color: #BFCE28 !important;
        border: 1px solid #BFCE28 !important;
    }
</style>
"""