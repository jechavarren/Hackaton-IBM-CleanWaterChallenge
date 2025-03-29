import json
import logging
import pandas as pd
import numpy as np
from typing import Literal, Optional
from langchain_core.output_parsers import JsonOutputParser

from models import ModelFactory
from prompts import PromptFactory


# Configure logging
logging.basicConfig(
    # filename='app.log',
    filemode="a",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

class AnalyzeWaterDataPipeline:
    """
    Pipeline to analyze water data.
    """
    def __init__(self):
        self.constant = 'constant'
    
    def generate_json_output(self, df):
        columns_elements = ['CLORO LIBRE RESIDUAL', 'CONDUCTIVIDAD (20ºC)', 'PH (20ºC)', 'TEMPERATURA', 'TURBIDEZ']
        
        def calculate_thresholds(filtered_df, elements, sampling_point_id):
            historical_df = filtered_df[:-1]
            data = {"sampling_point_id": sampling_point_id}
            
            for element in elements:
                Q1 = np.percentile(historical_df[element].dropna(), 25)
                Q2 = np.percentile(historical_df[element].dropna(), 50)
                Q3 = np.percentile(historical_df[element].dropna(), 75)
                IQR = Q3 - Q1
                
                lower_limit = Q1 - 1.5 * IQR
                upper_limit = Q3 + 1.5 * IQR
                lower_threshold = (Q2 + lower_limit) / 2
                upper_threshold = (Q2 + upper_limit) / 2
                
                data[f"{element}_min"] = Q1
                data[f"{element}_max"] = Q3
                data[f"{element}_median"] = Q2
            
            return pd.DataFrame([data])
        
        def verify_compliance(row, param):
            min_col = f"{param}_min"
            max_col = f"{param}_max"
            valor = row[param]
            min_val = row.get(min_col, 0)
            max_val = row.get(max_col, float("inf"))
            return "OK" if min_val <= valor <= max_val else "KO"
        
        def evaluate_elements(df, df_thresholds, columns_elements):
            last_date_measurements_df = df[-1:]
            df_merged = last_date_measurements_df.merge(df_thresholds, on="sampling_point_id")
            
            for param in columns_elements:
                df_merged[f"{param}_alert"] = df_merged.apply(lambda row: verify_compliance(row, param), axis=1)
            
            df_merged["Conclusion"] = df_merged[[f"{param}_alert" for param in columns_elements]].apply(lambda row: "OK" if all(row == "OK") else "KO", axis=1)
            return df_merged
        
        dfs_evaluate = []
        dfs_thresholds = []
        for i in df['sampling_point_id'].unique():
            filtered_df = df[df['sampling_point_id'] == i]
            df_thresholds = calculate_thresholds(filtered_df, columns_elements, i)
            df_evaluate = evaluate_elements(filtered_df, df_thresholds, columns_elements)
            dfs_evaluate.append(df_evaluate)
            dfs_thresholds.append(df_thresholds)
        
        final_df_evaluate = pd.concat(dfs_evaluate, ignore_index=True)
        final_df_thresholds = pd.concat(dfs_thresholds, ignore_index=True)
        conclusion = "OK" if (final_df_evaluate["Conclusion"] == "OK").all() else "KO"
        
        output = {
            "city": final_df_evaluate.iloc[0]['city'],
            "water_tank_name": final_df_evaluate.iloc[0]['sampling_point_name'],
            "alert": conclusion,
            "component": []
        }
        
        for param in columns_elements:
            output["component"].append({
                "name": param,
                "value": round(final_df_evaluate.iloc[0][param],3),
                "lower_threshold": round(final_df_thresholds.iloc[0][f"{param}_min"],3),
                "upper_threshold": round(final_df_thresholds.iloc[0][f"{param}_max"],3),
                "median": round(final_df_thresholds.iloc[0][f"{param}_median"],3),
                "component_alert": final_df_evaluate.iloc[0][f"{param}_alert"]
            })
        
        return json.dumps(output, indent=4, ensure_ascii=False)
    
    def analyze_water_data(self, water_data: pd.DataFrame):
        try:
            json_output = self.generate_json_output(water_data)
            return json.loads(json_output)
        except Exception as e:
            logging.error(f"Error processing water data: {str(e)}")
            return {"error": "Failed to analyze water data"}
        
    def sample_analyze_water_data(self):

        with open('data/water_data.json', 'r') as f:
            data = json.load(f)

        return data
