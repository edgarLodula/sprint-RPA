from src.process_pdf import processa_pdf


def main():
    PATH = r"./data/pdf/sprint_data.pdf"

    resultados=processa_pdf(PATH)

    return resultados
    
    
    

if __name__ == "__main__":
    main()