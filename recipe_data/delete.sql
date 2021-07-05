-- Delete Budget Bytes tables
delete from ingredients3;
delete from recipe_ingredients3;

-- Reset Budget Bytes tables
UPDATE `sqlite_sequence` SET `seq` = 0 WHERE `name` = 'recipe_ingredients3';
UPDATE `sqlite_sequence` SET `seq` = 0 WHERE `name` = 'ingredients3';