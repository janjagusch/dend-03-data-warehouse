insert into users
select user_id::INTEGER,
       first_name,
       last_name,
       gender,
       level
  from (select userid as user_id,
               firstname as first_name,
               lastname as last_name,
               gender,
               level
          from staging_events
         where user_id is not Null) as temp
 group by user_id, first_name, last_name, gender, level
 order by user_id;
