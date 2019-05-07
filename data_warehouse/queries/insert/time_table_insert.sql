insert into time
select start_time,
       date_part(hour, date_time) as hour,
       date_part(day, date_time) as day,
       date_part(week, date_time) as week,
       date_part(month, date_time) as month,
       date_part(year, date_time) as year,
       date_part(weekday, date_time) as weekday
  from (select ts as start_time,
               '1970-01-01'::date + ts/1000 * interval '1 second' as date_time
          from staging_events
         group by ts) as temp
 order by start_time;
