python manage.py shell
from django.contrib.auth.models import User
from news.models import *

# 1. Создать двух пользователей (с помощью метода User.objects.create_user('username')).
User.objects.create_user('Короткова М.')
User.objects.create_user('Губанов Э.')

# 2. Создать два объекта модели Author, связанные с пользователями.
Author.objects.create(author=User.objects.get(id=7))
Author.objects.create(author=User.objects.get(id=8))

# 3. Добавить 4 категории в модель Category.
Category.objects.create(categories = 'Спорт')
Category.objects.create(categories = 'Политика')
Category.objects.create(categories = 'Образование')
Category.objects.create(categories = 'Медицина')

# 4. Добавить 2 статьи и 1 новость.
Post.objects.create(author=Author.objects.get(id=1), type = 'AR',
                    text='Настоящая статья посвящена актуальной проблеме физической подготовки в процессе получения '
                         'высшего образования. В работе анализируются особенности подготовки студентов данной категории '
                         'обучения, рассмотрены пути преодоления отдельных проблем, возникающих ходе физической подготовки.',
                    title='ЗНАЧЕНИЕ И РОЛЬ СПОРТА В ВЫСШЕМ ОБРАЗОВАНИИ')
Post.objects.create(author=Author.objects.get(id=2), type = 'AR',
                    text='Объектом исследования является социальная политика государства. Предметом исследования - '
                         'коммерциализация системы здравоохранения в постсоветский период. В статье рассматриваются '
                         'такие вопросы как цели, механизмы реализации, практические результаты внедрения коммерческой '
                         'медицины в систему здравоохранения в контексте общей политики модернизации с учетом позиции '
                         'медицинских работников и граждан России.',
                    title='СОЦИАЛЬНАЯ ПОЛИТИКА ГОСУДАРСТВА: КОММЕРЦИАЛИЗАЦИЯ СИСТЕМЫ ЗДРАВООХРАНЕНИЯ В ПОСТСОВЕТСКИЙ ПЕРИОД')
Post.objects.create(author=Author.objects.get(id=2), type = 'NW',
                    text='Международная федерация хоккея (IIHF) запретила сборным России и Белоруссии участвовать в '
                         'чемпионате мира 2023 года.',
                    title='Сборным России и Белоруссии по хоккею запрещено участвовать в чемпионате мира 2023')

# 5. Присвоить им категории (как минимум в одной статье/новости должно быть не меньше 2 категорий).
p1 = Post.objects.get(id=1)
p2 = Post.objects.get(id=2)
p3 = Post.objects.get(id=3)
p1.category.add(Category.objects.get(id=1))
p1.category.add(Category.objects.get(id=3))
p2.category.add(Category.objects.get(id=2))
p2.category.add(Category.objects.get(id=4))
p3.category.add(Category.objects.get(id=1))
p3.category.add(Category.objects.get(id=2))

# 6. Создать как минимум 4 комментария к разным объектам модели Post (в каждом объекте должен быть как минимум один комментарий).

Comment.objects.create(post=Post.objects.get(id=1), author=User.objects.get(id=8), text='Комментарий')
Comment.objects.create(post=Post.objects.get(id=2), author=User.objects.get(id=7), text='Комментарий')
Comment.objects.create(post=Post.objects.get(id=3), author=User.objects.get(id=7), text='Комментарий')
Comment.objects.create(post=Post.objects.get(id=3), author=User.objects.get(id=7), text='Комментарий')

# 7. Применяя функции like() и dislike() к статьям/новостям и комментариям, скорректировать рейтинги этих объектов.

c1 = Comment.objects.get(id=1)
c2 = Comment.objects.get(id=2)
c3 = Comment.objects.get(id=3)
c4 = Comment.objects.get(id=4)

p1.like()
p1.like()
p1.like()
p2.like()
p3.like()
p1.dislike()
p2.dislike()
p2.dislike()
p2.dislike()
c2.like()
c2.like()
c4.dislike()

# 8. Обновить рейтинги пользователей.

for a in Author.objects.all():
    a.update_rating()

# 9. Вывести username и рейтинг лучшего пользователя (применяя сортировку и возвращая поля первого объекта).

Author.objects.all().order_by('-author_rating').values('author__username', 'author_rating')[0]

# 10. Вывести дату добавления, username автора, рейтинг, заголовок и превью лучшей статьи, основываясь на
# лайках/дислайках к этой статье.

best = Post.objects.filter(type='AR').order_by('-post_rating')[0]
best.time.date()
best.author.author.username
best.post_rating
best.title
best.preview()

# 11. Вывести все комментарии (дата, пользователь, рейтинг, текст) к этой статье.

Comment.objects.filter(post=best).values('time', 'author__username', 'comment_rating', 'text')



