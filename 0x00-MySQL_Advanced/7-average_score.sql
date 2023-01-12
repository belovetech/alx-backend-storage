-- creates a stored procedure ComputeAverageScoreForUser that computes and store the average score for a student.
-- Requirements:
-- Procedure ComputeAverageScoreForUser is taking 1 input:
-- user_id, a users.id value (you can assume user_id is linked to an existing users)
DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;
DELIMITER $$

CREATE PROCEDURE ComputeAverageScoreForUser(
    IN user_id INT)
BEGIN
    DECLARE avg_score FLOAT;
    SET avg_score = (SELECT AVG(score) FROM correction AS C where C.user_id=user_id);
    UPDATE users SET average_score = avg_score WHERE id=used_id;
END 
$$
DELIMITER ;