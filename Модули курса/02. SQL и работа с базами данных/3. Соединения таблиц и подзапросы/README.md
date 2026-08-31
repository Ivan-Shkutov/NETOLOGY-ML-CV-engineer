## Цель домашнего задания:

 1. закрепить навыки использования методов соединения таблиц с помощью разных вариаций JOIN.

 2. научиться формировать сложные конструкции запросов с помощью подзапросов.

### Работа выполняется в базе данных dvd-rental.


## Основная часть:

 ### Задание №1

Выведите для каждого покупателя его адрес проживания, город и страну проживания.

В результирующей таблице должны быть следующие столбцы: Имя пользователя, фамилия пользователя, адрес, город, страна.

```
select
    c.first_name as "Имя пользователя",
    c.last_name as "Фамилия пользователя",
    a.address as "Адрес",
    ci.city as "Город",
    co.country as "Страна"
from customer c
join address a on c.address_id = a.address_id
join city ci on a.city_id = ci.city_id
join country co on ci.country_id = co.country_id
order by c.customer_id;
```

```
Использовал:
 1. JOIN — для соединения таблиц по внешним ключам.
 2. cоединение идёт по цепочке:
    customer -> address -> city -> country.
 3. это гарантирует, что для каждого покупателя мы получаем его адрес, город и страну без дублирования строк.
```


 ### Задание №2.1

С помощью SQL-запроса посчитайте для каждого магазина количество его покупателей.

В результирующей таблице должны быть следующие столбцы: Идентификатор магазина, количество прикрепленных пользователей.

```
select
    store_id as "Идентификатор магазина",
    count(customer_id) as "Количество прикрепленных пользователей"
from customer
group by store_id
order by store_id;
```

```
Использовал:
1. GROUP BY — группировка покупателей по магазинам.
2. COUNT(customer_id) — подсчёт количества покупателей в каждом магазине.
```


 ### Задание №2.2

Доработайте запрос и выведите только те магазины, у которых количество покупателей больше 300-от.

Для решения используйте фильтрацию по сгруппированным строкам с использованием функции агрегации.

В результирующей таблице должны быть следующие столбцы: Идентификатор магазина, количество прикрепленных пользователей.

```
select
    store_id as "Идентификатор магазина",
    count(customer_id) as "Количество прикрепленных пользователей"
from customer
group by store_id
having count(customer_id) > 300
order by store_id;
```

```
Использовал:
1. HAVING — фильтрация уже сгруппированных строк.
2. Условие COUNT(customer_id) > 300 оставляет только магазины, у которых больше 300 покупателей.
```


 ### Задание №2.3

Доработайте запрос, добавив в него информацию о городе магазина, а также фамилию и имя продавца, который работает в этом магазине.

В результирующей таблице должны быть следующие столбцы: Фамилия и имя сотрудника в виде одного значения, идентификатор магазина, город нахождения магазина, количество прикрепленных пользователей.

```
select
    s.first_name || ' ' || s.last_name as "Фамилия и имя сотрудника",
    st.store_id as "Идентификатор магазина",
    ci.city as "Город нахождения магазина",
    count(c.customer_id) as "Количество прикрепленных пользователей"
from store st
join staff s on st.manager_staff_id = s.staff_id
join address a on st.address_id = a.address_id
join city ci on a.city_id = ci.city_id
join customer c on c.store_id = st.store_id
group by st.store_id, ci.city, s.first_name, s.last_name
having count(c.customer_id) > 300
order by st.store_id;
```

```
Использовал:
1. JOIN для получения данных о сотруднике, адресе и городе магазина.
2. конкатенация first_name || ' ' || last_name — формируем единое значение «Фамилия и имя сотрудника».
3. GROUP BY — группировка по магазину, городу и сотруднику.
4. HAVING COUNT(...) > 300 — оставляем только магазины с более чем 300 покупателями.
```


 ### Задание №3

Для каждого фильма посчитайте сколько раз его брали в прокат, при этом работать нужно только с теми фильмами, в которых снимались актрисы с именем Julia.

В результирующей таблице должны быть следующие столбцы: Название фильма, количество аренд.

```
select
    f.title as "Название фильма",
    count(r.rental_id) as "Количество аренд"
from film f
join film_actor fa on f.film_id = fa.film_id
join actor a on fa.actor_id = a.actor_id
join inventory i on f.film_id = i.film_id
join rental r on i.inventory_id = r.inventory_id
where a.first_name = 'Julia'
group by f.film_id, f.title
order by "Количество аренд" desc, f.title;
```

```
Использовал:
1. JOIN для прохождения по цепочке:
   film -> film_actor -> actor -> inventory -> rental.
2. WHERE a.first_name = 'Julia' — отбираем только фильмы с актрисами по имени Julia.
3. GROUP BY f.film_id, f.title — группируем по каждому фильму.
4. COUNT(r.rental_id) — считаем количество аренд.
5. ORDER BY count desc — наглядная сортировка по востребованности.
```


 ### Задание №4

Посчитайте для каждого покупателя 4 аналитических показателя:

 - количество фильмов, которые он взял в аренду

 - общую стоимость платежей за аренду всех фильмов (значение округлите до целого числа)

 - минимальное значение платежа за аренду фильма

 - максимальное значение платежа за аренду фильма

В результирующей таблице должны быть следующие столбцы: Фамилия и имя пользователя в виде одного значения, количество арендованных фильмов, округленная сумма платежей, минимальный и максимальный платеж.

```
select
    c.first_name || ' ' || c.last_name as "Фамилия и имя пользователя",
    coalesce(r.rental_count, 0) as "Количество арендованных фильмов",
    coalesce(round(p.total_amount), 0) as "Округленная сумма платежей",
    coalesce(p.min_payment, 0) as "Минимальный платеж",
    coalesce(p.max_payment, 0) as "Максимальный платеж"
from customer c
left join (
    select
        customer_id,
        count(rental_id) as rental_count
    from rental
    group by customer_id
) r on r.customer_id = c.customer_id
left join (
    select
        customer_id,
        sum(amount) as total_amount,
        min(amount) as min_payment,
        max(amount) as max_payment
    from payment
    group by customer_id
) p on p.customer_id = c.customer_id
order by c.customer_id;
```

```
Использовал:
1. подзапросы для раздельной агрегации по rental и payment. Это позволяет избежать ложного роста количества строк.
2. COUNT(rental_id) — количество аренд.
3. SUM(amount) — общая сумма платежей.
4. ROUND(...) — округление до целого числа.
5. MIN(amount), MAX(amount) — минимальный и максимальный платёж.
6. COALESCE — для корректного отображения покупателей без аренд/платежей.
```



 ### Задание №5

Используя данные из таблицы городов, составьте все возможные пары городов так, чтобы в результате не было пар с одинаковыми названиями городов. Решение должно быть через Декартово произведение.

В результирующей таблице должны быть следующие столбцы: два столбца с названиями городов.

```
select
    c1.city as "Город 1",
    c2.city as "Город 2"
from city c1
cross join city c2
where c1.city != c2.city
  and c1.city < c2.city
order by c1.city, c2.city;
```

```
Использовал:
1. CROSS JOIN — декартово произведение таблицы городов саму на себя.
2. условие c1.city != c2.city исключает пары одинаковых городов.
3. условие c1.city < c2.city исключает зеркальные дубли: например, если была пара (A, B), то не будет пары (B, A).
```



 ### Задание №6

Выведите наиболее и наименее востребованные категории фильмов (те, которые арендовали наибольшее/наименьшее количество раз), количество аренд и сумму продаж.

В результирующей таблице должны быть следующие столбцы: Название категории, количество аренд, сумма продаж.

```
with category_stats as (
    select
        cat.category_id,
        cat.name as category_name,
        count(r.rental_id) as rental_count,
        sum(p.amount) as total_sales
    from category cat
    join film_category fc on cat.category_id = fc.category_id
    join film f on fc.film_id = f.film_id
    join inventory i on f.film_id = i.film_id
    join rental r on i.inventory_id = r.inventory_id
    join payment p on r.rental_id = p.rental_id
    group by cat.category_id, cat.name
)
select
    category_name as "Название категории",
    rental_count as "Количество аренд",
    total_sales as "Сумма продаж"
from category_stats
where rental_count = (select max(rental_count) from category_stats)
   or rental_count = (select min(rental_count) from category_stats)
order by rental_count desc;
```

```
Использовал:
1. CTE (category_stats) — промежуточная агрегированная таблица.
2. соединение category -> film_category -> film -> inventory -> rental -> payment.
3. COUNT(rental_id) — количество аренд по категории.
4. SUM(amount) — сумма продаж по категории.
5. подзапросы с MAX(...) и MIN(...) — нахождение самых востребованных и самых невостребованных категорий.
```




 
