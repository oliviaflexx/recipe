-- Delete Budget Bytes tables
delete from recipes2;
delete from ingredients2;
delete from recipe_ingredients2;

-- Reset Budget Bytes tables
UPDATE `sqlite_sequence` SET `seq` = 0 WHERE `name` = 'recipes2';
UPDATE `sqlite_sequence` SET `seq` = 0 WHERE `name` = 'recipe_ingredients2';
UPDATE `sqlite_sequence` SET `seq` = 0 WHERE `name` = 'ingredients2';