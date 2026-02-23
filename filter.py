import os

def filter_logins(keyword, filename):
    filtered_logins = []
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            if keyword in line:
                filtered_logins.append(line.strip())

    return filtered_logins

def sanitize_keyword(keyword):
    return keyword.replace(":", "_")

def main():
    list_filename = input("Load List: ")
    with open('host_config.txt', 'r', encoding='ISO-8859-1') as config_file:
        keywords = config_file.read().splitlines()

    for keyword in keywords:
        filtered_logins = filter_logins(keyword, list_filename)
        sanitized_keyword = sanitize_keyword(keyword)
        if filtered_logins:
            output_filename = f"{sanitized_keyword}-{len(filtered_logins)}.txt"
            with open(output_filename, "w", encoding="utf-8") as output_file:
                output_file.write("\n".join(filtered_logins))
            print(f"Configs: '{keyword}' - Found {len(filtered_logins)} logins")
        else:
            print(f"Configs: '{keyword}' - Found 0 logins")

if __name__ == "__main__":
    main()
