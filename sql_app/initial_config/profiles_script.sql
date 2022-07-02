INSERT INTO public.profiles(
	id, name, min_score, can_comment, can_evaluate_movies,
    can_read, can_answer_comments, can_mention_comments,
    can_evaluate_comments, can_delete_comments, can_mark_comment_as_repeated,
    can_turn_user_into_moderator)
	VALUES (0, 'Leitor', 0, FALSE, TRUE, TRUE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE);

INSERT INTO public.profiles(
	id, name, min_score, can_comment, can_evaluate_movies,
    can_read, can_answer_comments, can_mention_comments,
    can_evaluate_comments, can_delete_comments, can_mark_comment_as_repeated,
    can_turn_user_into_moderator)
	VALUES (1, 'Básico', 20, TRUE, TRUE, TRUE, TRUE, FALSE, FALSE, FALSE, FALSE, FALSE);

INSERT INTO public.profiles(
	id, name, min_score, can_comment, can_evaluate_movies,
    can_read, can_answer_comments, can_mention_comments,
    can_evaluate_comments, can_delete_comments, can_mark_comment_as_repeated,
    can_turn_user_into_moderator)
	VALUES (2, 'Avançado', 100, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, FALSE, FALSE, FALSE);

   INSERT INTO public.profiles(
	id, name, min_score, can_comment, can_evaluate_movies,
    can_read, can_answer_comments, can_mention_comments,
    can_evaluate_comments, can_delete_comments, can_mark_comment_as_repeated,
    can_turn_user_into_moderator)
	VALUES (3, 'Moderador', 1000, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE);

