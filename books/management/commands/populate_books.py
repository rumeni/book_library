from django.core.management.base import BaseCommand
from books.models import Book


class Command(BaseCommand):
    help = 'Populate the database with famous books'

    def handle(self, *args, **options):
        # Clear existing books
        Book.objects.all().delete()
        
        famous_books = [
            # J.K. Rowling - Harry Potter Series
            {
                'title': 'Harry Potter and the Philosopher\'s Stone',
                'author': 'J.K. Rowling',
                'isbn': '978-0747532699',
                'publication_date': '1997-06-26',
                'genre': 'Fantasy',
                'description': 'The first book in the Harry Potter series follows young Harry as he discovers he is a wizard and begins his magical education at Hogwarts School of Witchcraft and Wizardry.'
            },
            {
                'title': 'Harry Potter and the Chamber of Secrets',
                'author': 'J.K. Rowling',
                'isbn': '978-0747538493',
                'publication_date': '1998-07-02',
                'genre': 'Fantasy',
                'description': 'Harry\'s second year at Hogwarts brings new challenges as the Chamber of Secrets is opened and students are being petrified by a mysterious monster.'
            },
            {
                'title': 'Harry Potter and the Prisoner of Azkaban',
                'author': 'J.K. Rowling',
                'isbn': '978-0747542155',
                'publication_date': '1999-07-08',
                'genre': 'Fantasy',
                'description': 'Harry learns about his past and faces the escaped prisoner Sirius Black, who is believed to be after him.'
            },
            
            # George Orwell
            {
                'title': '1984',
                'author': 'George Orwell',
                'isbn': '978-0451524935',
                'publication_date': '1949-06-08',
                'genre': 'Dystopian Fiction',
                'description': 'A dystopian novel set in a totalitarian society ruled by Big Brother, exploring themes of surveillance, truth, and individual freedom.'
            },
            {
                'title': 'Animal Farm',
                'author': 'George Orwell',
                'isbn': '978-0451526342',
                'publication_date': '1945-08-17',
                'genre': 'Political Satire',
                'description': 'An allegorical novella about farm animals who rebel against their human farmer, hoping to create a society where animals can be equal, free, and happy.'
            },
            
            # Harper Lee
            {
                'title': 'To Kill a Mockingbird',
                'author': 'Harper Lee',
                'isbn': '978-0061120084',
                'publication_date': '1960-07-11',
                'genre': 'Southern Gothic',
                'description': 'A coming-of-age story set in the American South, dealing with serious issues of rape and racial inequality through the eyes of young Scout Finch.'
            },
            
            # F. Scott Fitzgerald
            {
                'title': 'The Great Gatsby',
                'author': 'F. Scott Fitzgerald',
                'isbn': '978-0743273565',
                'publication_date': '1925-04-10',
                'genre': 'American Literature',
                'description': 'A critique of the American Dream set in the Jazz Age, following the mysterious millionaire Jay Gatsby and his obsession with Daisy Buchanan.'
            },
            
            # Jane Austen
            {
                'title': 'Pride and Prejudice',
                'author': 'Jane Austen',
                'isbn': '978-0141439518',
                'publication_date': '1813-01-28',
                'genre': 'Romance',
                'description': 'A romantic novel following Elizabeth Bennet as she navigates issues of manners, upbringing, morality, education, and marriage in Georgian England.'
            },
            {
                'title': 'Sense and Sensibility',
                'author': 'Jane Austen',
                'isbn': '978-0141439662',
                'publication_date': '1811-10-30',
                'genre': 'Romance',
                'description': 'The story of the Dashwood sisters, Elinor and Marianne, who represent "sense" and "sensibility" respectively, as they navigate love and heartbreak.'
            },
            
            # Ernest Hemingway
            {
                'title': 'The Old Man and the Sea',
                'author': 'Ernest Hemingway',
                'isbn': '978-0684801223',
                'publication_date': '1952-09-01',
                'genre': 'Literary Fiction',
                'description': 'The story of an aging Cuban fisherman who struggles with a giant marlin far out in the Gulf Stream off the coast of Cuba.'
            },
            {
                'title': 'A Farewell to Arms',
                'author': 'Ernest Hemingway',
                'isbn': '978-0684837888',
                'publication_date': '1929-09-27',
                'genre': 'War Fiction',
                'description': 'A semi-autobiographical novel about an American ambulance driver in the Italian army during World War I and his love affair with a British nurse.'
            },
            
            # Agatha Christie
            {
                'title': 'Murder on the Orient Express',
                'author': 'Agatha Christie',
                'isbn': '978-0062693662',
                'publication_date': '1934-01-01',
                'genre': 'Mystery',
                'description': 'Hercule Poirot investigates a murder aboard the famous Orient Express train, where every passenger becomes a suspect.'
            },
            {
                'title': 'And Then There Were None',
                'author': 'Agatha Christie',
                'isbn': '978-0062073488',
                'publication_date': '1939-11-06',
                'genre': 'Mystery',
                'description': 'Ten strangers are invited to an island where they are killed one by one, following the pattern of a sinister nursery rhyme.'
            },
            {
                'title': 'The Murder of Roger Ackroyd',
                'author': 'Agatha Christie',
                'isbn': '978-0062073563',
                'publication_date': '1926-06-01',
                'genre': 'Mystery',
                'description': 'Hercule Poirot investigates the murder of Roger Ackroyd in a case that revolutionized the mystery genre with its shocking twist.'
            },
            
            # Stephen King
            {
                'title': 'The Shining',
                'author': 'Stephen King',
                'isbn': '978-0307743657',
                'publication_date': '1977-01-28',
                'genre': 'Horror',
                'description': 'A family heads to an isolated hotel for the winter where a sinister presence influences the father into violence, while his psychic son sees horrific forebodings.'
            },
            {
                'title': 'It',
                'author': 'Stephen King',
                'isbn': '978-1501142970',
                'publication_date': '1986-09-15',
                'genre': 'Horror',
                'description': 'A group of children in a small town discover that their worst nightmares are real when they face an ancient evil that emerges every 27 years.'
            },
            {
                'title': 'Carrie',
                'author': 'Stephen King',
                'isbn': '978-0307743664',
                'publication_date': '1974-04-05',
                'genre': 'Horror',
                'description': 'Stephen King\'s first published novel tells the story of Carrie White, a teenage girl with telekinetic powers who is bullied at school and abused at home.'
            },
            
            # Tolkien
            {
                'title': 'The Hobbit',
                'author': 'J.R.R. Tolkien',
                'isbn': '978-0547928227',
                'publication_date': '1937-09-21',
                'genre': 'Fantasy',
                'description': 'Bilbo Baggins, a hobbit, is swept into an epic quest to reclaim the lost Dwarf Kingdom of Erebor from the fearsome dragon Smaug.'
            },
            {
                'title': 'The Fellowship of the Ring',
                'author': 'J.R.R. Tolkien',
                'isbn': '978-0547928210',
                'publication_date': '1954-07-29',
                'genre': 'Fantasy',
                'description': 'The first volume of The Lord of the Rings follows Frodo Baggins as he begins his quest to destroy the One Ring and defeat the Dark Lord Sauron.'
            },
            {
                'title': 'The Two Towers',
                'author': 'J.R.R. Tolkien',
                'isbn': '978-0547928203',
                'publication_date': '1954-11-11',
                'genre': 'Fantasy',
                'description': 'The second volume continues the epic journey as the Fellowship is broken and the members face their individual challenges in the war against Sauron.'
            },
            
            # Dan Brown
            {
                'title': 'The Da Vinci Code',
                'author': 'Dan Brown',
                'isbn': '978-0307474278',
                'publication_date': '2003-03-18',
                'genre': 'Thriller',
                'description': 'Symbologist Robert Langdon investigates a murder in the Louvre and discovers a battle between the Priory of Sion and Opus Dei over the possibility of Jesus having been married.'
            },
            {
                'title': 'Angels & Demons',
                'author': 'Dan Brown',
                'isbn': '978-0671027360',
                'publication_date': '2000-05-01',
                'genre': 'Thriller',
                'description': 'Robert Langdon races against time to prevent the Illuminati from destroying Vatican City with a powerful new weapon - antimatter.'
            },
            
            # Paulo Coelho
            {
                'title': 'The Alchemist',
                'author': 'Paulo Coelho',
                'isbn': '978-0062315007',
                'publication_date': '1988-01-01',
                'genre': 'Philosophical Fiction',
                'description': 'A young Andalusian shepherd travels from Spain to Egypt in search of a treasure, discovering the importance of following one\'s dreams.'
            },
            
            # Gabriel García Márquez
            {
                'title': 'One Hundred Years of Solitude',
                'author': 'Gabriel García Márquez',
                'isbn': '978-0060883287',
                'publication_date': '1967-06-05',
                'genre': 'Magical Realism',
                'description': 'The multi-generational story of the Buendía family, whose patriarch founded the fictional town of Macondo, in the jungles of Colombia.'
            },
            
            # Victor Hugo
            {
                'title': 'Les Misérables',
                'author': 'Victor Hugo',
                'isbn': '978-0451419439',
                'publication_date': '1862-01-01',
                'genre': 'Historical Fiction',
                'description': 'Set in early 19th-century France, the novel follows the lives and interactions of several characters, particularly the struggles of ex-convict Jean Valjean and his path to redemption.'
            },
            {
                'title': 'The Hunchback of Notre-Dame',
                'author': 'Victor Hugo',
                'isbn': '978-0140443530',
                'publication_date': '1831-01-14',
                'genre': 'Gothic Fiction',
                'description': 'Set in medieval Paris, the story revolves around the beautiful gypsy Esmeralda, the hunchbacked bell-ringer Quasimodo, and the archdeacon Claude Frollo.'
            },
            
            # Leo Tolstoy
            {
                'title': 'War and Peace',
                'author': 'Leo Tolstoy',
                'isbn': '978-0199232765',
                'publication_date': '1869-01-01',
                'genre': 'Historical Fiction',
                'description': 'An epic novel that chronicles the French invasion of Russia and the impact of the Napoleonic era on Tsarist society through the stories of five Russian aristocratic families.'
            },
            {
                'title': 'Anna Karenina',
                'author': 'Leo Tolstoy',
                'isbn': '978-0143035008',
                'publication_date': '1877-01-01',
                'genre': 'Literary Fiction',
                'description': 'The tragic story of the married aristocrat Anna Karenina and her affair with the affluent Count Vronsky, which leads to her ultimate downfall.'
            },
            
            # Charles Dickens
            {
                'title': 'A Tale of Two Cities',
                'author': 'Charles Dickens',
                'isbn': '978-0486406510',
                'publication_date': '1859-11-26',
                'genre': 'Historical Fiction',
                'description': 'Set in London and Paris before and during the French Revolution, the novel tells the story of the French Doctor Manette and his daughter Lucie.'
            },
            {
                'title': 'Great Expectations',
                'author': 'Charles Dickens',
                'isbn': '978-0141439563',
                'publication_date': '1861-08-01',
                'genre': 'Bildungsroman',
                'description': 'The coming-of-age story of Pip, an orphan who rises from humble beginnings to wealth and status, only to learn valuable lessons about love and loyalty.'
            },
            {
                'title': 'Oliver Twist',
                'author': 'Charles Dickens',
                'isbn': '978-0141439747',
                'publication_date': '1838-01-01',
                'genre': 'Social Criticism',
                'description': 'The story of an orphan boy who escapes from a workhouse and falls in with a gang of juvenile pickpockets in London.'
            },
            
            # Mark Twain
            {
                'title': 'The Adventures of Huckleberry Finn',
                'author': 'Mark Twain',
                'isbn': '978-0486280615',
                'publication_date': '1884-12-10',
                'genre': 'Adventure',
                'description': 'Huck Finn escapes his abusive father and travels down the Mississippi River with Jim, a runaway slave, in this classic American novel.'
            },
            {
                'title': 'The Adventures of Tom Sawyer',
                'author': 'Mark Twain',
                'isbn': '978-0486400778',
                'publication_date': '1876-01-01',
                'genre': 'Adventure',
                'description': 'The mischievous adventures of Tom Sawyer, a young boy growing up along the Mississippi River in the fictional town of St. Petersburg, Missouri.'
            },
            
            # Arthur Conan Doyle
            {
                'title': 'The Adventures of Sherlock Holmes',
                'author': 'Arthur Conan Doyle',
                'isbn': '978-0486474915',
                'publication_date': '1892-10-14',
                'genre': 'Mystery',
                'description': 'A collection of twelve short stories featuring the brilliant detective Sherlock Holmes and his loyal companion Dr. Watson.'
            },
            {
                'title': 'The Hound of the Baskervilles',
                'author': 'Arthur Conan Doyle',
                'isbn': '978-0486282145',
                'publication_date': '1902-04-01',
                'genre': 'Mystery',
                'description': 'Sherlock Holmes investigates the legend of a supernatural hound that haunts the Baskerville family on the foggy moors of Dartmoor.'
            },
            
            # Fyodor Dostoevsky
            {
                'title': 'Crime and Punishment',
                'author': 'Fyodor Dostoevsky',
                'isbn': '978-0486415871',
                'publication_date': '1866-01-01',
                'genre': 'Psychological Fiction',
                'description': 'The psychological drama of Raskolnikov, a poor student who commits murder and then struggles with guilt and redemption.'
            },
            {
                'title': 'The Brothers Karamazov',
                'author': 'Fyodor Dostoevsky',
                'isbn': '978-0374528379',
                'publication_date': '1880-01-01',
                'genre': 'Philosophical Fiction',
                'description': 'The final novel by Dostoevsky explores deep philosophical and theological themes through the story of the Karamazov family.'
            },
            
            # Oscar Wilde
            {
                'title': 'The Picture of Dorian Gray',
                'author': 'Oscar Wilde',
                'isbn': '978-0486278070',
                'publication_date': '1890-07-01',
                'genre': 'Gothic Fiction',
                'description': 'A young man sells his soul for eternal youth and beauty while his portrait ages and reflects his moral corruption.'
            },
            
            # Bram Stoker
            {
                'title': 'Dracula',
                'author': 'Bram Stoker',
                'isbn': '978-0486411095',
                'publication_date': '1897-05-26',
                'genre': 'Gothic Horror',
                'description': 'The classic vampire novel that introduced Count Dracula and established many conventions of subsequent vampire fantasy.'
            },
            
            # Mary Shelley
            {
                'title': 'Frankenstein',
                'author': 'Mary Shelley',
                'isbn': '978-0486282114',
                'publication_date': '1818-01-01',
                'genre': 'Gothic Science Fiction',
                'description': 'Victor Frankenstein creates a creature assembled from dead body parts, but the creature becomes a monster that haunts his creator.'
            },
            
            # Jules Verne
            {
                'title': 'Twenty Thousand Leagues Under the Sea',
                'author': 'Jules Verne',
                'isbn': '978-0486266299',
                'publication_date': '1870-01-01',
                'genre': 'Science Fiction',
                'description': 'Professor Aronnax and his companions are taken prisoner aboard Captain Nemo\'s submarine Nautilus and experience incredible underwater adventures.'
            },
            {
                'title': 'Around the World in Eighty Days',
                'author': 'Jules Verne',
                'isbn': '978-0486411118',
                'publication_date': '1873-01-01',
                'genre': 'Adventure',
                'description': 'Phileas Fogg makes a bet that he can travel around the world in eighty days, leading to a thrilling race against time.'
            },
            
            # H.G. Wells
            {
                'title': 'The Time Machine',
                'author': 'H.G. Wells',
                'isbn': '978-0486284729',
                'publication_date': '1895-05-07',
                'genre': 'Science Fiction',
                'description': 'A Victorian scientist travels to the year 802,701 AD and discovers a world divided between the peaceful Eloi and the predatory Morlocks.'
            },
            {
                'title': 'The War of the Worlds',
                'author': 'H.G. Wells',
                'isbn': '978-0486295060',
                'publication_date': '1898-01-01',
                'genre': 'Science Fiction',
                'description': 'Martians invade Earth with advanced technology, causing widespread destruction until they are defeated by Earth\'s bacteria.'
            },
            
            # Ray Bradbury
            {
                'title': 'Fahrenheit 451',
                'author': 'Ray Bradbury',
                'isbn': '978-1451673319',
                'publication_date': '1953-10-19',
                'genre': 'Dystopian Fiction',
                'description': 'In a future society where books are outlawed and burned, a fireman begins to question his role and the society he serves.'
            },
            
            # Kurt Vonnegut
            {
                'title': 'Slaughterhouse-Five',
                'author': 'Kurt Vonnegut',
                'isbn': '978-0440180296',
                'publication_date': '1969-03-31',
                'genre': 'Anti-war Fiction',
                'description': 'Billy Pilgrim experiences time non-linearly, witnessing his own life including his experiences as a prisoner of war during the bombing of Dresden.'
            },
            
            # Ken Kesey
            {
                'title': 'One Flew Over the Cuckoo\'s Nest',
                'author': 'Ken Kesey',
                'isbn': '978-0452284654',
                'publication_date': '1962-02-01',
                'genre': 'Psychological Fiction',
                'description': 'Randle McMurphy, a new patient at a mental institution, clashes with the oppressive Nurse Ratched in this critique of institutional authority.'
            },
        ]
        
        created_count = 0
        for book_data in famous_books:
            try:
                book = Book.objects.create(**book_data)
                created_count += 1
                self.stdout.write(f"Created: {book.title} by {book.author}")
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"Error creating {book_data['title']}: {str(e)}")
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} books!')
        )
