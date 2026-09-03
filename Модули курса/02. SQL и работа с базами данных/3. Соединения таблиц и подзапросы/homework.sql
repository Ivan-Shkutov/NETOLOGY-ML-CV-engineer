--============================================================
-- Домашнее задание
-- База данных: dvd-rental
-- Тема: соединения таблиц и подзапросы
--============================================================

SET search_path TO public;

--============================================================
-- Задание №1
-- Для каждого покупателя вывести адрес проживания, город и страну.
--============================================================

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


--============================================================
-- Задание №2.1
-- Количество покупателей по каждому магазину.
--============================================================

select
    store_id as "Идентификатор магазина",
    count(customer_id) as "Количество прикрепленных пользователей"
from customer
group by store_id
order by store_id;


--============================================================
-- Задание №2.2
-- Магазины, у которых количество покупателей больше 300.
--============================================================

select
    store_id as "Идентификатор магазина",
    count(customer_id) as "Количество прикрепленных пользователей"
from customer
group by store_id
having count(customer_id) > 300
order by store_id;


--============================================================
-- Задание №2.3
-- Магазины с покупателями больше 300, городом и сотрудником.
--============================================================

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


--============================================================
-- Задание №3
-- Количество аренд фильмов с актрисами по имени Julia.
--============================================================

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


--============================================================
-- Задание №4
-- Аналитические показатели по каждому покупателю.
--============================================================

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


--============================================================
-- Задание №5
-- Все возможные пары городов через декартово произведение.
--============================================================

select
    c1.city as "Город 1",
    c2.city as "Город 2"
from city c1
cross join city c2
where c1.city != c2.city
  and c1.city < c2.city
order by c1.city, c2.city;


--============================================================
-- Задание №6
-- Наиболее и наименее востребованные категории фильмов.
--============================================================

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