from src.data.input_parser import parse_input
import src.db.db as db

def main():
    print("Welcome to your cats database!")
    while True:
        user_input = input("Enter a command: ")
        possible_commands = """Possible commands:
        read all - shows all the records from DB
        read {name} - shows the record with name = {name} 
        update {name} age {value} - replaces age for cat {name} with {value}
        update {name} features {values} - adds a new feature for cat {name} if it does not exist, entering multiple features allowed (separated by ',')
        delete all - deletes all the records
        delete {name} - deletes cat {name} record
        add {name} - adds a new cat {name}, after adding a new cat record the details (age, features) are requested through consol
        hello
        close
        exit
        """
        command, *args = parse_input(user_input)

        try:

            if command in ["close", "exit"]:
                print("Good bye!")
                break

            elif command == "hello":
                print("How can I help you?")

            elif command == "read" and args[0] == "all": 
                # shows all the records from DB
                for el in db.read_all():
                    print(el)

            elif command == "read":
                # shows the record with name = args[0]
                print(db.read_by_name(args[0]))

            elif command == "update" and args[1] == "age": 
                # replaces age for cat name = args[0] with {value}
                result = db.update_age(args[0], int(args[2]))
                if result:
                    print(f"Cat record {args[0]} updated: \n{result}")
                else:
                    create_user_input = input(f"Cat record {args[0]} doesn't exist. Do you want to create it? Enter yes/no: ")
                    if create_user_input == "yes":
                        create_new_cat(args[0])

            elif command == "update" and args[1] == "features":
                # adds a new feature for cat {name} if it does not exist, entering multiple features allowed (separated by ',')
                features = " ".join(args[2:])
                for feature in features.split(","):
                    db.update_features(args[0], feature.strip())
                if db.read_by_name(args[0]):
                    print(f"Cat record {args[0]} updated: ")
                    print(db.read_by_name(args[0]))
                else: 
                    create_user_input = input(f"Cat record {args[0]} doesn't exist. Do you want to create it? Enter yes/no: ")
                    if create_user_input == 'yes':
                        create_new_cat(args[0])

            elif command == "delete" and args[0] == "all":
                # deletes all the records
                db.delete_all()
                print('All the records deleted')

            elif command == "delete":
                # deletes cat with name = args[0] record
                if db.read_by_name(args[0]):
                    print(f"Cat record {args[0]} deleted.")
                else:
                    print(f"Cat record {args[0]} doesn't exist")
                db.delete_by_name(args[0])

            elif command == "add":
                create_new_cat(args[0])

            else:
                print(f"Invalid command. {possible_commands}")

        except IndexError:
            print(
                f"Please make sure you have entered all the required arguments. {possible_commands}"
            )


def create_new_cat(name: str):
    # adds a new cat {name}, after adding a new cat record the details (age, features) are requested through consol
    db.add_new_cat(name)
    age = input("Enter cat's age (or press Enter): ")
    if age:
        db.update_age(name, int(age))
    features = input("Enter cat's features (or press Enter): ")
    if features:
        for feature in features.split(","):
            db.update_features(name, feature.strip())



if __name__ == "__main__":
    main()
