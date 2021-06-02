delete from recipe;
delete from ingredients;
delete from recipe_ingredients;


UPDATE `sqlite_sequence` SET `seq` = 0 WHERE `name` = 'recipe';
UPDATE `sqlite_sequence` SET `seq` = 0 WHERE `name` = 'recipe_ingredients';
UPDATE `sqlite_sequence` SET `seq` = 0 WHERE `name` = 'ingredients';