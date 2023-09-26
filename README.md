## О данном проекте 
* Back-end для магазина чего-угодно на чистом Django
* Есть ещё недочёты, но решил уже открыть репозиторий

### Запуск
1. Клонируем проект с репозитория
```python
https://github.com/yottabufer/PureDjangoShop.git
```
2. Переходим в папку созданную папку
```python
cd PureDjangoShop
```
3. Создаём виртуально окружение для работы с проектом
```python
python -m venv venv_PureDjangoShop
```
4. Активируем виртуальное окружение
	
+ Linux
```python
source venv_PureDjangoShop/bin/activate
```
+ Windows
```python
venv_PureDjangoShop\Scripts\activate.bat 
```
5. Устанавливаем зависимости
```python
pip install -r requirements.txt
```
6. Создаем и накатываем миграции 
```python
python manage.py makemigrations 
```
и
```python
python manage.py migrate 
```

7. Генерируем магазины и товары к ним
```python
python manage.py shop_create
```
и
```python
python manage.py product_create
```
8. Pапускаем
```python
python manage.py runserver
```
