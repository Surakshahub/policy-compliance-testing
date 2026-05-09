def load_prompt(file_path):

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    except Exception as e:
        print("Prompt Load Error:", e)
        return None