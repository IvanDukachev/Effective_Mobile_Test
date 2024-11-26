import json


DATA_FILE = "library.json"


class Book:
    def __init__(
            self,
            book_id: int,
            title: str,
            author: str,
            year: int,
            status: str="в наличии"
    ):
        """
        Initializes a Book object.

        Args:
            book_id (int): ID of the book.
            title (str): Title of the book.
            author (str): Author of the book.
            year (int): Year of the book.
            status (str, optional): Status of the book. Defaults to "в наличии".

        Returns:
            None
        """
        self.id = book_id
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def to_dict(self) -> dict[str, str | int]:
        """
        Converts the book to a dictionary.

        This method returns a dictionary with the following keys: "id", "title", "author", "year", "status".

        Returns:
            dict[str, str | int]: A dictionary with the books data.
        """
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status,
        }


class Library:
    def __init__(self):
        """
        Initializes a Library object.

        This method creates an empty list of books and calls `load_data` to fill it with the data from the file.

        Returns:
            None
        """
        self.books: list[Book] = []
        self.load_data()

    def load_data(self) -> None:
        """
        Loads the library from the file.

        This method reads the file and fills the list of books with the data from the file.

        Returns:
            None
        """
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            self.books = [Book(item["id"], item["title"], item["author"], item["year"]) for item in json.load(file)]

    def save_data(self) -> None:
        """
        Saves the current state of the library to the file.

        This method writes the current list of books to the file in JSON format.

        Returns:
            None
        """
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump([book.to_dict() for book in self.books], file, ensure_ascii=False, indent=2)

    def add_book(self, title: str, author: str, year: int) -> None:
        """
        Adds a new book to the library.

        Args:
            title (str): Title of the book to add.
            author (str): Author of the book to add.
            year (int): Year of the book to add;

        Returns:
            None
        """
        book_id = max((book.id for book in self.books), default=0) + 1
        new_book = Book(book_id, title, author, year)
        self.books.append(new_book)
        self.save_data()
        print(f"Книга '{title}' добавлена с ID {book_id}.")

    def remove_book(self, book_id: int) -> None:
        """
        Removes a book with the given ID from the library.

        Args:
            book_id (int): ID of the book to remove;

        Returns:
            None
        """
        book = next((book for book in self.books if book.id == book_id), None)
        if book:
            self.books.remove(book)
            self.save_data()
            print(f"Книга с ID {book_id} удалена.")
        else:
            print("Книга с таким ID не найдена.")

    def search_books(self, query:str , field: str) -> None:
        """
        Search books by query in specified field.

        Args:
            query (str): Query to search.
            field (str): Field to search in.

        Returns:
            None
        """
        results = [book for book in self.books if query.lower() in str(getattr(book, field, "")).lower()]
        if results:
            for book in results:
                print(book.to_dict())
        else:
            print("Книги не найдены.")

    def display_books(self) -> None:
        """Displays all books in the library.

        If the library is empty, print a message about it.
        Otherwise, print each book as a dictionary.
        """

        if not self.books:
            print("Библиотека пуста.")
        else:
            for book in self.books:
                print(book.to_dict())

    def update_status(self, book_id: int, status: str) -> None:
        """
        Updates the status of a book with the given ID.

        Args:
            book_id (int): ID of the book to update.
            status (str): New status of the book. Must be one of ["в наличии", "выдана"];

        Returns:
            None
        """
        book = next((book for book in self.books if book.id == book_id), None)
        if book:
            if status in ["в наличии", "выдана"]:
                book.status = status
                self.save_data()
                print(f"Статус книги ID {book_id} обновлен на '{status}'.")
            else:
                print("Некорректный статус.")
        else:
            print("Книга не найдена.")


def main() -> None:
    library = Library()

    while True:
        print("\nМеню:")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Найти книгу")
        print("4. Показать все книги")
        print("5. Изменить статус книги")
        print("6. Выйти")
        choice = input("Выберите действие: ")

        if choice == "1":
            try:
                title = input("Введите название книги: ")
                author = input("Введите автора книги: ")
                year = int(input("Введите год издания книги: "))
                if year < 0:
                    raise ValueError
                library.add_book(title, author, year)
            except ValueError:
                print("Год должен быть числом и больше нуля")
        elif choice == "2":
            book_id = int(input("Введите ID книги: "))
            library.remove_book(book_id)
        elif choice == "3":
            field = input("Искать по (title, author, year): ")
            query = input("Введите запрос: ")
            library.search_books(query, field)
        elif choice == "4":
            library.display_books()
        elif choice == "5":
            try:
                book_id = int(input("Введите ID книги: "))
            except ValueError:
                print("Id должен быть числом")
            status = input("Введите новый статус (в наличии/выдана): ")
            library.update_status(book_id, status)
        elif choice == "6":
            print("Выход")
            break
        else:
            print("Некорректный ввод. Попробуйте снова.")

if __name__ == "__main__":
    main()