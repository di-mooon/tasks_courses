--СОЗДАНИЕ УЗЛА:
----$right_ key – правый ключ родительского узла или максимальный правый ключ плюс единица
----$level – уровень родительского узла, либо 0, если родительского нет.
    update my_tree set
        right_key = right_key + $right_key,
        left_key = case
                        when left_key > $right_key then left_key + 2
                        else left_key
                   end
    where right_key >= $right_key;


    insert into my_tree
        (id,left_key, right_key, level, name)
        values
        ($id,$right_key,$right_key+1,$level, $name);


--УДАЛЕНИЕ УЗЛА:
----$left_key – левый ключ удаляемого узла
----$right_key – правый ключ
    delete from my_tree where left_key >= $left_key and right_key <= $right_key;
    update my_tree set
        left_key = case
                        when left_key > $left_key then left_key - ($right_key - $left_key + 1)
                        else left_key
                   end,
        right_key = right_key – ($right_key - $left_key + 1)
    WHERE right_key > $right_key

--ПЕРЕМЕЩЕНИЕ УЗЛА:
----$level, $left_key, $right_key - ключи перемещаемого узла
----$level_up
----$right_key_near, $left_key_near - ключи cтарого родительского узла
----$skew_level = $level_up - $level + 1  - смещение уровня изменяемого узла;
----$skew_tree = $right_key - $left_key + 1 - смещение ключей дерева;
----$skew_edit = &right_key_near - $left_key + 1 - $skew_tree - смещение ключей редактируемого узла
----$id_edit - список id номеров перемещаемой ветки.

--Вверх по дереву:
    update my_table set
    right_key =case
                    when left_key >= $left_key then right_key + $skew_edit
                    else
                        case
                            when right_key < $left_key then right_key + $skew_tree
                            else right_key
                        end
                end,
    level = CASE
                WHEN left_key >= $left_key THEN level + $skew_level
                ELSE level
            END,
    left_key = case
                    when left_key >= $left_key then left_key + $skew_edit
                    else
                        case
                            when left_key > $right_key_near then left_key + $skew_tree
                             else left_key
                        end
               end
    where right_key > $right_key_near and left_key < $right_key
