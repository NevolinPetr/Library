from requests import get, post

print(get('http://localhost:5000/api/book/1').json())
print('')
print(post('http://localhost:5000/api/book',
           json={'title': 'Тёмные начала',
                 'author': '',
                 'annotation': '«Северное сияние» — первая книга трилогии «Тёмные начала». Поиски пропавшего друга ',
                 'genre_id': 1,
                 'created_date': 1995,
                 'img_file': 'C:/Users/GS-8/Downloads/his_dark_materials.img',
                 'text_file': 'C:/Users/GS-8/Downloads/his_dark_materials.fb2'
                 }
           ).json())
