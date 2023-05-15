from shops_parser import Parser
from excel_table import Excel_table

from threading import Thread
import time


COUNT_THREADS = 2

TABLE_PATH = "ozon.xlsx"

def main(requests):
    
    for request in requests:
        table = Excel_table(TABLE_PATH, sheet_name=request[3])
        parsers = []
        for i in range (COUNT_THREADS):
            parser = Parser (base_url=request[0], step=COUNT_THREADS, start_page=request[1] + i, last_page=request[2], table= table)
            parsers.append(parser)
            
            thread = Thread(target=parser.parsing)
            thread.start()
            
        while True:
            time.sleep(10)
            is_all_executed = True
            for parser in parsers:

                if not parser.is_executed:
                    is_all_executed = False
                    
            if is_all_executed:
                table.save_table()   
                break
         
            
if __name__ == "__main__":
    # request by category:
    #[url, start_page, last_page, categoty_name]
    requests = [
            # [
            #     "ozon",
            #     "https://www.ozon.ru/category/flakony-dorozhnye-6691/?category_was_predicted=true&deny_category_prediction=true&from_global=true&text=%D0%B4%D0%BE%D1%80%D0%BE%D0%B6%D0%BD%D1%8B%D0%B5+%D1%84%D0%BB%D0%B0%D0%BA%D0%BE%D0%BD%D1%8B",
            #     11,
            #     30,
            #     "Флаконы Дорожные"
            # ],
            # [
            #     "ozon", 
            #     "https://www.ozon.ru/category/aksessuary-dlya-ochishcheniya-litsa-6334/?tf_state=85oj0x1501ONB4z4LMHaeWyAVglvjQcVrs1Ld-T-nlCZPxWy",
            #     1,
            #     8,
            #     "Аксессуары для очищения лица"
            # ],
            # [
            #     "ozon", 
            #     "https://www.ozon.ru/category/aksessuary-dlya-ochishcheniya-litsa-6334/?tf_state=85oj0x1501ONB4z4LMHaeWyAVglvjQcVrs1Ld-T-nlCZPxWy",
            #     9,
            #     16,
            #     "Аксессуары для очищения лица"
            # ],
            [ 
                "https://www.ozon.ru/category/aksessuary-dlya-ochishcheniya-litsa-6334/?tf_state=85oj0x1501ONB4z4LMHaeWyAVglvjQcVrs1Ld-T-nlCZPxWy",
                17,
                22,
                "Аксессуары для очищения лица"
            ],
            [
                "https://www.ozon.ru/category/aksessuary-dlya-ochishcheniya-litsa-6334/?tf_state=85oj0x1501ONB4z4LMHaeWyAVglvjQcVrs1Ld-T-nlCZPxWy",
                23,
                28,
                "Аксессуары для очищения лица"
            ],
            
            
        ]
    
    main(requests=requests)
    
    

