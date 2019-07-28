## what_can_you_do
* what_can_you_do
  - action_what_I_can_do

## news
* newsfeed
  - utter_newsfeed

## happy path
* greet
  - utter_greet
* mood_great
  - utter_happy

## sad path 1
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up

## sad path 2
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up

## say goodbye
* goodbye
  - utter_goodbye

## thanks
* thank_you
  - utter_no_problem

## ok
* ok
  - utter_cool

## nevermind
* deny
  - utter_cool
  - action_reset_slots
  - slot{"portfolio_query":null,"name":null,"amount_query":null,"amount":null}

## give_general_advice_give_general_advice
* ask_general_advice
  - action_give_general_advice
  - slot{"name":"Aricka Lewis","portfolio_query":"followed"}
* ask_general_advice
  - action_give_general_advice
  - slot{"name":"Benjamin Parker","portfolio_query":"not_followed"}
  - action_reset_slots

## give_general_advice_give_follow_advice
* ask_general_advice
  - action_give_general_advice
  - slot{"name":"Aricka Lewis","portfolio_query":"followed"}
* ask_follow_advice
  - action_give_following_advice
  - slot{"name":"Alois Reiter","portfolio_query":"not_followed"}
  - action_reset_slots

## give_general_advice_give_unfollow_advice
* ask_general_advice
  - action_give_general_advice
  - slot{"name":"Aricka Lewis","portfolio_query":"followed"}
* ask_unfollow_advice
  - action_give_following_advice
  - slot{"name":"Florianne Paget","portfolio_query":"followed"}
  - action_reset_slots

## give_general_advice_should_i_follow
* ask_general_advice
  - action_give_general_advice
  - slot{"name":"Aricka Lewis","portfolio_query":"followed"}
* should_i_follow
  - action_fetch_portfolio
  - slot{"portfolio_query":"not_followed","name":"Benjamin Parker"}
  - action_should_i_follow_advice
  - action_reset_slots

## give_general_advice_should_i_unfollow
* ask_general_advice
  - action_give_general_advice
  - slot{"name":"Paulinho Simoes","portfolio_query":"followed"}
* should_i_unfollow
  - action_fetch_portfolio
  - slot{"portfolio_query":"followed","name":"William Shore"}
  - action_should_i_unfollow_advice
  - action_reset_slots

## give_general_advice_follow
* ask_general_advice
  - action_give_general_advice
  - slot{"name":"Aricka Lewis","portfolio_query":"not_followed"}
* follow
  - action_fetch_portfolio
  - slot{"name":"Aricka Lewis","portfolio_query":"not_followed","amount_query":null,"amount":null}
  - action_ask_add_amount
* amount
  - action_follow
  - action_reset_slots
  - slot{"portfolio_query":null,"name":null,"amount_query":null,"amount":null}

## give_general_advice_follow_him_her
* ask_general_advice
  - action_give_general_advice
  - slot{"name":"Aricka Lewis","portfolio_query":"not_followed"}
* follow_him_her
  - action_ask_add_amount
* amount
  - action_follow
  - action_reset_slots
  - slot{"portfolio_query":null,"name":null,"amount_query":null,"amount":null}

## give_general_advice_follow_do_it
* ask_general_advice
  - action_give_general_advice
  - slot{"name":"Aricka Lewis","portfolio_query":"not_followed"}
* do_it
  - slot{"name":"Aricka Lewis","portfolio_query":"not_followed"}
  - action_ask_add_amount
* amount
  - action_follow
  - action_reset_slots
  - slot{"portfolio_query":null,"name":null,"amount_query":null,"amount":null}

## give_general_advice_unfollow
* ask_general_advice
  - action_give_general_advice
  - slot{"name":"Aricka Lewis","portfolio_query":"followed"}
* unfollow
  - action_fetch_portfolio
  - slot{"name":"Aricka Lewis","portfolio_query":"followed","amount_query":null,"amount":null}
  - action_unfollow
  - action_reset_slots

## give_general_advice_unfollow_him_her
* ask_general_advice
  - action_give_general_advice
  - slot{"name":"Masami Nishimura","portfolio_query":"followed"}
* unfollow_him_her
  - action_unfollow
  - action_reset_slots

## give_general_advice_unfollow_do_it
* ask_general_advice
  - action_give_general_advice
  - slot{"name":"Paulinho Simoes","portfolio_query":"followed"}
* do_it
  - slot{"name":"Paulinho Simoes","portfolio_query":"followed"}
  - action_unfollow
  - action_reset_slots

## give_general_advice_unfollow_do_it
* ask_general_advice
  - action_give_general_advice
  - slot{"name":"Alois Reiter","portfolio_query":"followed"}
* do_it
  - slot{"name":"Alois Reiter","portfolio_query":"followed"}
  - action_unfollow
  - action_reset_slots




## give_follow_advice_give_follow_advice
* ask_follow_advice
  - action_give_following_advice
  - slot{"name":"Andrzej Kraviec"}
* ask_follow_advice
  - action_give_following_advice
  - slot{"name":"Florianne Paget"}
  - action_reset_slots

## give_follow_advice_give_unfollow_advice
* ask_follow_advice
  - action_give_following_advice
  - slot{"name":"Paulinho Simoes"}
* ask_unfollow_advice
  - action_give_unfollowing_advice
  - slot{"name":"Aricka Lewis"}
  - action_reset_slots

## give_follow_advice_with_follow
* ask_follow_advice
  - action_give_following_advice
  - slot{"name":"Andrzej Kraviec"}
* follow_him_her
  - action_ask_add_amount
  - slot{"name":"Andrzej Kraviec"}
* amount
  - action_follow
  - action_reset_slots

## give_follow_advice_with_follow_do_it
* ask_follow_advice
  - action_give_following_advice
  - slot{"name":"Andrzej Kraviec"}
* do_it
  - action_ask_add_amount
  - slot{"name":"Andrzej Kraviec"}
* amount
  - action_follow
  - action_reset_slots

## give_follow_advice_with_add_amount
* ask_follow_advice
  - action_give_following_advice
  - slot{"name":"William Shore"}
* add_amount_to_him_her
  - action_follow
  - action_reset_slots

## give_follow_advice_with_add
* ask_follow_advice
  - action_give_following_advice
  - slot{"name":"William Shore"}
* add_to_him_her
  - action_ask_add_amount
* amount
  - action_follow
  - action_reset_slots



## give_unfollow_advice_give_unfollow_advice
* ask_unfollow_advice
  - action_give_unfollowing_advice
  - slot{"name":"Ralph Axelsen"}
* ask_unfollow_advice
  - action_give_unfollowing_advice
  - slot{"name":"William Shore"}
  - action_reset_slots

## give_unfollow_advice_give_follow_advice
* ask_unfollow_advice
  - action_give_unfollowing_advice
  - slot{"name":"Benjamin Parker"}
* ask_follow_advice
  - action_give_following_advice
  - slot{"name":"Benjamin Parker"}
  - action_reset_slots

## give_unfollow_advice_with_unfollow
* ask_unfollow_advice
  - action_give_unfollowing_advice
  - slot{"name":"Aricka Lewis"}
* unfollow_him_her
  - action_unfollow
  - action_reset_slots

## give_unfollow_advice_with_unfollow
* ask_unfollow_advice
  - action_give_unfollowing_advice
  - slot{"name":"Aricka Lewis"}
* do_it
  - action_unfollow
  - action_reset_slots

## give_unfollow_advice_with_withdraw_amount
* ask_unfollow_advice
  - action_give_unfollowing_advice
  - slot{"name":"Masami Nishimura"}
* withdraw_amount_from_him_her
  - action_withdraw_amount
  - action_reset_slots



## follow_successful
* follow
  - action_fetch_portfolio
  - slot{"portfolio_query":"not_followed","name":"Aricka Lewis"}
  - action_ask_add_amount
* amount
  - action_follow
  - action_reset_slots
  - slot{"portfolio_query":null,"name":null,"amount_query":null,"amount":null}

## follow_invalid_name
* follow
  - action_fetch_portfolio
  - slot{"portfolio_query":"invalid","name":"Jeremy"}
  - utter_invalid_portfolio
  - action_reset_slots
  - slot{"portfolio_query":null,"name":null,"amount_query":null,"amount":null}

## follow_null
* follow
  - action_fetch_portfolio
  - slot{"portfolio_query":null,"name":null}
  - utter_invalid_portfolio
  - action_reset_slots
  - slot{"portfolio_query":null,"name":null,"amount_query":null,"amount":null}

## follow_already_followed
* follow
  - action_fetch_portfolio
  - slot{"portfolio_query":"followed","name":"Alois Reiter"}
  - utter_already_followed_portfolio
  - action_reset_slots
  - slot{"portfolio_query":null,"name":null,"amount_query":null,"amount":null}



## unfollow_successful
* unfollow
  - action_fetch_portfolio
  - slot{"portfolio_query":"followed","name":"Masami Nishimura"}
  - action_unfollow
  - action_reset_slots
  - slot{"portfolio_query":null,"name":null,"amount_query":null,"amount":null}

## unfollow_not_followed
* unfollow
  - action_fetch_portfolio
  - slot{"portfolio_query":"not_followed","name":"Paulinho Simoes"}
  - utter_already_not_followed_portfolio
  - action_reset_slots
  - slot{"portfolio_query":null,"name":null,"amount_query":null,"amount":null}

## unfollow_invalid_name
* unfollow
  - action_fetch_portfolio
  - slot{"portfolio_query":"invalid","name":"John"}
  - utter_invalid_portfolio
  - action_reset_slots
  - slot{"portfolio_query":null,"name":null,"amount_query":null,"amount":null}

## unfollow_null
* unfollow
  - action_fetch_portfolio
  - slot{"portfolio_query":null,"name":null}
  - utter_invalid_portfolio
  - action_reset_slots
  - slot{"portfolio_query":null,"name":null,"amount_query":null,"amount":null}



## add_amount_to_not_followed_successful
* add_amount
  - action_fetch_portfolio
  - slot{"portfolio_query":"not_followed","name":"Florianne Paget","amount_query":"valid","amount":"50.00"}
  - action_follow
  - action_reset_slots
  - slot{"portfolio_query":null,"name":null,"amount_query":null,"amount":null}

## add_amount_to_not_followed_successful
* add_amount
  - action_fetch_portfolio
  - slot{"portfolio_query":"not_followed","name":"Florianne Paget", "amount_query":null,"amount":null}
  - action_ask_add_amount
* amount
  - action_follow
  - action_reset_slots
  - slot{"portfolio_query":null,"name":null,"amount_query":null,"amount":null}

## add_amount_to_followed_successful
* add_amount
  - action_fetch_portfolio
  - slot{"portfolio_query":"followed","name":"Ralph Axelsen","amount_query":"valid","amount":"100"}
  - action_add_amount
  - action_reset_slots
  - slot{"portfolio_query":null,"name":null,"amount_query":null,"amount":null}

## add_amount_to_followed_successful
* add_amount
  - action_fetch_portfolio
  - slot{"portfolio_query":"followed","name":"Andrzej Kraviec","amount_query":null,"amount":null}
  - action_ask_add_amount
* amount
  - action_add_amount
  - action_reset_slots
  - slot{"portfolio_query":null,"name":null,"amount_query":null,"amount":null}

## add_amount_invalid_name
* add_amount
  - action_fetch_portfolio
  - slot{"portfolio_query":"invalid","name":"shrek"}
  - utter_invalid_portfolio
  - action_reset_slots
  - slot{"portfolio_query":null,"name":null,"amount_query":null,"amount":null}

## add_amount_null_name
* add_amount
  - action_fetch_portfolio
  - slot{"portfolio_query":null,"name":null}
  - utter_invalid_portfolio
  - action_reset_slots
  - slot{"portfolio_query":null,"name":null,"amount_query":null,"amount":null}

## add_amount_invalid_amount
* add_amount
  - action_fetch_portfolio
  - slot{"amount_query":"invalid","name":"Andrzej Kraviec","amount":"-12.00"}
  - utter_invalid_amount
  - action_reset_slots
  - slot{"portfolio_query":null,"name":null,"amount_query":null,"amount":null}

## add_amount_null_amount
* add_amount
  - action_fetch_portfolio
  - slot{"portfolio_query":"not_followed","name":"Masami Nishimura","amount_query":null,"amount":null}
  - utter_invalid_amount
  - action_reset_slots
  - slot{"portfolio_query":null,"name":null,"amount_query":null,"amount":null}



## withdraw_amount_successful
* withdraw_amount
  - action_fetch_portfolio
  - slot{"portfolio_query":"followed","name":"Alois Reiter","amount_query":"valid","amount":"50"}
  - action_withdraw_amount
  - action_reset_slots

## withdraw_amount_successful
* withdraw_amount
  - action_fetch_portfolio
  - slot{"portfolio_query":"followed","name":"Alois Reiter","amount_query":null,"amount":null}
  - action_ask_withdraw_amount
* amount
  - slot{"portfolio_query":"followed","name":"Alois Reiter","amount_query":null,"amount":null}
  - action_withdraw_amount
  - action_reset_slots

## withdraw_amount_invalid_name
* withdraw_amount
  - action_fetch_portfolio
  - slot{"portfolio_query":"invalid","name":"Mark Ritz","amount_query":"valid","amount":"10.00"}
  - utter_invalid_portfolio
  - action_reset_slots

## withdraw_amount_null_name
* withdraw_amount
  - action_fetch_portfolio
  - slot{"portfolio_query":null,"name":null}
  - utter_invalid_portfolio
  - action_reset_slots

## withdraw_amount_not_followed
* withdraw_amount
  - action_fetch_portfolio
  - slot{"portfolio_query":"not_followed","name":"William Shore","amount_query":"valid","amount":"65.50"}
  - utter_already_not_followed_portfolio
  - action_reset_slots

## withdraw_from_successful
* withdraw_from
  - action_fetch_portfolio
  - slot{"portfolio_query":"followed","name":"Florianne Paget","amount_query":null,"amount":null}
  - action_ask_withdraw_amount
* amount
  - action_withdraw_amount
  - action_reset_slots

## withdraw_from_successful
* withdraw_from
  - action_fetch_portfolio
  - slot{"portfolio_query":"followed","name":"Florianne Paget","amount_query":null,"amount":null}
  - action_ask_withdraw_amount
* amount
  - action_withdraw_amount
  - action_reset_slots



## unfollow_everyone_affirmed
* unfollow_everyone
  - utter_are_you_sure_unfollow_everyone
* affirm
  - action_unfollow_everyone

## unfollow_everyone_do_it
* unfollow_everyone
  - utter_are_you_sure_unfollow_everyone
* do_it
  - action_unfollow_everyone

## unfollow_everyone_denied
* unfollow_everyone
  - utter_are_you_sure_unfollow_everyone
* deny
  - utter_okay



## follow_everyone
* follow_everyone
  - utter_please_follow_one_portfolio_at_a_time



## should_i_follow_should_i_follow
* should_i_follow
  - action_fetch_portfolio
  - slot{"portfolio_query":"not_followed","name":"Benjamin Parker"}
  - action_should_i_follow_advice
* should_i_follow
  - action_fetch_portfolio
  - slot{"portfolio_query":"not_followed","name":"Alois Reiter"}
  - action_should_i_follow_advice
  - action_reset_slots

## should_i_follow_should_i_unfollow
* should_i_follow
  - action_fetch_portfolio
  - slot{"portfolio_query":"not_followed","name":"Benjamin Parker"}
  - action_should_i_follow_advice
* should_i_unfollow
  - action_fetch_portfolio
  - slot{"portfolio_query":"followed","name":"Alois Reiter"}
  - action_should_i_unfollow_advice
  - action_reset_slots

## should_i_follow_should_i_unfollow
* should_i_follow
  - action_fetch_portfolio
  - slot{"portfolio_query":"followed","name":"Alois Reiter"}
  - action_should_i_follow_advice
* should_i_unfollow
  - action_fetch_portfolio
  - slot{"portfolio_query":"followed","name":"Benjamin Parker"}
  - action_should_i_unfollow_advice
  - action_reset_slots

## should_i_follow_invalid
* should_i_follow
  - action_fetch_portfolio
  - slot{"portfolio_query":"invalid","name":"Daniel"}
  - utter_invalid_portfolio
  - action_reset_slots

## should_i_follow_none
* should_i_follow
  - action_fetch_portfolio
  - slot{"portfolio_query":null,"name":null}
  - utter_invalid_portfolio
  - action_reset_slots

## should_i_follow_with_follow_successful
* should_i_follow
  - action_fetch_portfolio
  - slot{"portfolio_query":"not_followed","name":"Benjamin Parker"}
  - action_should_i_follow_advice
* follow_him_her
  - action_ask_add_amount
  - slot{"name":"Benjamin Parker"}
* amount
  - action_follow
  - action_reset_slots

## should_i_follow_with_follow_do_it_successful
* should_i_follow
  - action_fetch_portfolio
  - slot{"portfolio_query":"not_followed","name":"Benjamin Parker"}
  - action_should_i_follow_advice
* do_it
  - action_ask_add_amount
  - slot{"name":"Benjamin Parker"}
* amount
  - action_follow
  - action_reset_slots

## should_i_follow_with_follow_already_followed
* should_i_follow
  - action_fetch_portfolio
  - slot{"portfolio_query":"followed","name":"Benjamin Parker"}
  - action_should_i_follow_advice
* follow_him_her
  - utter_already_followed_portfolio
  - action_reset_slots

## should_i_follow_with_follow_do_it_already_followed
* should_i_follow
  - action_fetch_portfolio
  - slot{"portfolio_query":"followed","name":"Benjamin Parker"}
  - action_should_i_follow_advice
* do_it
  - utter_already_followed_portfolio
  - action_reset_slots

## should_i_follow_with_unfollow_successful
* should_i_follow
  - action_fetch_portfolio
  - slot{"portfolio_query":"followed","name":"Andrzej Kraviec"}
  - action_should_i_follow_advice
* unfollow_him_her
  - slot{"portfolio_query":"followed","name":"Andrzej Kraviec"}
  - action_unfollow
  - action_reset_slots

## should_i_follow_with_unfollow_already_not_followed
* should_i_follow
  - action_fetch_portfolio
  - slot{"portfolio_query":"not_followed","name":"Andrzej Kraviec"}
  - action_should_i_follow_advice
* unfollow_him_her
  - slot{"portfolio_query":"not_followed","name":"Andrzej Kraviec"}
  - utter_already_not_followed_portfolio
  - action_reset_slots

## should_i_follow_followed_with_add_amount
* should_i_follow
  - action_fetch_portfolio
  - slot{"portfolio_query":"followed","name":"Ralph Axelsen","amount_query":null,"amount":null}
  - action_should_i_follow_advice
* add_amount_to_him_her
  - slot{"portfolio_query":"followed","name":"Ralph Axelsen","amount_query":null,"amount":null}
  - action_add_amount
  - action_reset_slots

## should_i_follow_followed_with_add_to_him
* should_i_follow
  - action_fetch_portfolio
  - slot{"portfolio_query":"followed","name":"Benjamin Parker","amount_query":null,"amount":null}
  - action_should_i_follow_advice
* add_to_him_her
  - slot{"portfolio_query":"followed","name":"Benjamin Parker","amount_query":null,"amount":null}
  - action_ask_add_amount
* amount
  - action_add_amount
  - action_reset_slots

## should_i_follow_not_followed_with_add_amount
* should_i_follow
  - action_fetch_portfolio
  - slot{"portfolio_query":"not_followed","name":"Masami Nishimura","amount_query":null,"amount":null}
  - action_should_i_follow_advice
* add_amount_to_him_her
  - action_follow
  - action_reset_slots

## should_i_follow_with_withdraw_amount_followed
* should_i_follow
  - action_fetch_portfolio
  - slot{"portfolio_query":"followed","name":"Florianne Paget"}
  - action_should_i_follow_advice
* withdraw_amount_from_him_her
  - action_withdraw_amount
  - action_reset_slots

## should_i_follow_with_withdraw_from_him_followed
* should_i_follow
  - action_fetch_portfolio
  - slot{"portfolio_query":"followed","name":"Florianne Paget"}
  - action_should_i_follow_advice
* withdraw_from_him_her
  - slot{"portfolio_query":"followed","name":"Florianne Paget"}
  - action_ask_withdraw_amount
* amount
  - action_withdraw_amount
  - action_reset_slots

## should_i_follow_with_withdraw_amount_not_followed
* should_i_follow
  - action_fetch_portfolio
  - slot{"portfolio_query":"not_followed","name":"Florianne Paget"}
  - action_should_i_follow_advice
* withdraw_amount_from_him_her
  - utter_already_not_followed_portfolio
  - action_reset_slots

## should_i_follow_with_withdraw_from_him_her_not_followed
* should_i_follow
  - action_fetch_portfolio
  - slot{"portfolio_query":"not_followed","name":"Florianne Paget"}
  - action_should_i_follow_advice
* withdraw_from_him_her
  - utter_already_not_followed_portfolio
  - action_reset_slots



## should_i_unfollow_should_i_unfollow
* should_i_unfollow
  - action_fetch_portfolio
  - slot{"portfolio_query":"followed","name":"Paulinho Simoes"}
  - action_should_i_unfollow_advice
* should_i_unfollow
  - action_fetch_portfolio
  - slot{"portfolio_query":"followed","name":"Paulinho Simoes"}
  - action_should_i_unfollow_advice
  - action_reset_slots

## should_i_unfollow_should_i_follow
* should_i_unfollow
  - action_fetch_portfolio
  - slot{"portfolio_query":"followed","name":"Florianne Paget"}
  - action_should_i_unfollow_advice
* should_i_follow
  - action_fetch_portfolio
  - slot{"portfolio_query":"not_followed","name":"Kanya Bunnag"}
  - action_should_i_follow_advice
  - action_reset_slots

## should_i_unfollow_invalid
* should_i_follow
  - action_fetch_portfolio
  - slot{"portfolio_query":"invalid","name":"Max Jasper"}
  - utter_invalid_portfolio
  - action_reset_slots

## should_i_unfollow_none
* should_i_unfollow
  - action_fetch_portfolio
  - slot{"portfolio_query":null,"name":null}
  - utter_invalid_portfolio
  - action_reset_slots

## should_i_unfollow_with_unfollow_successful
* should_i_unfollow
  - action_fetch_portfolio
  - slot{"portfolio_query":"followed","name":"Paulinho Simoes"}
  - action_should_i_unfollow_advice
* unfollow_him_her
  - action_unfollow
  - action_reset_slots

## should_i_unfollow_with_unfollow_do_it_successful
* should_i_unfollow
  - action_fetch_portfolio
  - slot{"portfolio_query":"followed","name":"Paulinho Simoes"}
  - action_should_i_unfollow_advice
* do_it
  - action_unfollow
  - action_reset_slots

## should_i_unfollow_with_unfollow_already_not_followed
* should_i_unfollow
  - action_fetch_portfolio
  - slot{"portfolio_query":"not_followed","name":"Paulinho Simoes"}
  - utter_already_not_followed_portfolio
  - action_reset_slots

## should_i_unfollow_with_add_amount
* should_i_unfollow
  - action_fetch_portfolio
  - slot{"portfolio_query":"followed","name":"Kanya Bunnag"}
  - action_should_i_unfollow_advice
* add_amount_to_him_her
  - action_add_amount
  - action_reset_slots

## should_i_unfollow_with_withdraw_amount
* should_i_unfollow
  - action_fetch_portfolio
  - slot{"portfolio_query":"followed","name":"William Shore"}
  - action_should_i_unfollow_advice
* withdraw_amount_from_him_her
  - action_withdraw_amount
  - action_reset_slots



## should_i_add_amount_should_i_add_amount
* should_i_add_amount
  - action_fetch_portfolio
  - slot{"portfolio_query":"followed","name":"Benjamin Parker"}
  - action_should_i_follow_advice
* should_i_add_amount
  - action_fetch_portfolio
  - slot{"portfolio_query":"followed","name":"Kanya Bunnag"}
  - action_should_i_follow_advice
  - action_reset_slots

## should_i_add_amount_should_i_follow
* should_i_add_amount
  - action_fetch_portfolio
  - slot{"portfolio_query":"followed","name":"Alois Reiter"}
  - action_should_i_follow_advice
* should_i_follow
  - action_fetch_portfolio
  - slot{"portfolio_query":"not_followed","name":"Masami Nishimura"}
  - action_should_i_follow_advice
  - action_reset_slots

## should_i_add_amount_should_i_unfollow
* should_i_add_amount
  - action_fetch_portfolio
  - slot{"portfolio_query":"followed","name":"Florianne Paget"}
  - action_should_i_follow_advice
* should_i_unfollow
  - action_fetch_portfolio
  - slot{"portfolio_query":"followed","name":"Masami Nishimura"}
  - action_should_i_unfollow_advice
  - action_reset_slots

## should_i_add_amount_invalid
* should_i_add_amount
  - action_fetch_portfolio
  - slot{"portfolio_query":"invalid","name":"Jack"}
  - utter_invalid_portfolio
  - action_reset_slots

## should_i_add_amount_none
* should_i_add_amount
  - action_fetch_portfolio
  - slot{"portfolio_query":null,"name":null}
  - utter_invalid_portfolio
  - action_reset_slots

## should_i_add_amount_followed_with_add_amount_successful
* should_i_add_amount
  - action_fetch_portfolio
  - slot{"portfolio_query":"followed","name":"Benjamin Parker"}
  - action_should_i_follow_advice
* add_amount_to_him_her
  - action_add_amount
  - action_reset_slots

## should_i_add_amount_not_followed_with_add_amount_successful
* should_i_add_amount
  - action_fetch_portfolio
  - slot{"portfolio_query":"not_followed","name":"Benjamin Parker"}
  - action_should_i_follow_advice
* add_amount_to_him_her
  - action_follow
  - action_reset_slots

## should_i_add_amount_followed_with_add_successful
* should_i_add_amount
  - action_fetch_portfolio
  - slot{"portfolio_query":"followed","name":"Kanya Bunnag"}
  - action_should_i_follow_advice
* add_to_him_her
  - slot{"portfolio_query":"followed","name":"Kanya Bunnag"}
  - action_ask_add_amount
* amount
  - action_add_amount
  - action_reset_slots

## should_i_add_amount_followed_with_add_successful
* should_i_add_amount
  - action_fetch_portfolio
  - slot{"portfolio_query":"followed","name":"Kanya Bunnag"}
  - action_should_i_follow_advice
* do_it
  - action_ask_add_amount
  - slot{"portfolio_query":"followed","name":"Kanya Bunnag"}
* amount
  - action_add_amount
  - action_reset_slots

## should_i_add_amount_not_followed_with_add_successful
* should_i_add_amount
  - action_fetch_portfolio
  - slot{"portfolio_query":"not_followed","name":"Kanya Bunnag"}
  - action_should_i_follow_advice
* add_to_him_her
  - action_ask_add_amount
  - slot{"portfolio_query":"followed","name":"Kanya Bunnag"}
* amount
  - action_follow
  - action_reset_slots

## should_i_add_amount_not_followed_with_add_successful
* should_i_add_amount
  - action_fetch_portfolio
  - slot{"portfolio_query":"not_followed","name":"Kanya Bunnag","amount_query":null,"amount":null}
  - action_should_i_follow_advice
* do_it
  - action_ask_add_amount
  - slot{"portfolio_query":"followed","name":"Kanya Bunnag"}
* amount
  - action_follow
  - action_reset_slots

## should_i_add_amount_not_followed_with_add_successful
* should_i_add_amount
  - action_fetch_portfolio
  - slot{"portfolio_query":"not_followed","name":"Kanya Bunnag","amount_query":"valid","amount":"50"}
  - action_should_i_follow_advice
* do_it
  - action_follow
  - action_reset_slots

## should_i_add_amount_followed_with_add_successful
* should_i_add_amount
  - action_fetch_portfolio
  - slot{"portfolio_query":"followed","name":"Kanya Bunnag","amount_query":"valid","amount":"100"}
  - action_should_i_follow_advice
* do_it
  - action_add_amount
  - action_reset_slots

## should_i_add_amount_invalid_name
* should_i_add_amount
  - action_fetch_portfolio
  - slot{"portfolio_query":"invalid","name":"George Smith"}
  - utter_invalid_portfolio
  - action_reset_slots

## should_i_add_amount_null_name
* should_i_add_amount
  - action_fetch_portfolio
  - slot{"portfolio_query":null,"name":null}
  - utter_invalid_portfolio
  - action_reset_slots

## should_i_add_amount_invalid_amount
* should_i_add_amount
  - action_fetch_portfolio
  - slot{"amount_query":"invalid","amount":"-48.239"}
  - utter_invalid_amount
  - action_reset_slots



## should_i_withdraw_amount_not_followed_should_i_withdraw_amount_not_followed
* should_i_withdraw_amount
  - action_fetch_portfolio
  - slot{"portfolio_query":"not_followed","name":"Benjamin Parker"}
  - utter_already_not_followed_portfolio
* should_i_withdraw_amount
  - action_fetch_portfolio
  - slot{"portfolio_query":"not_followed","name":"Kanya Bunnag"}
  - utter_already_not_followed_portfolio
  - action_reset_slots

## should_i_withdraw_amount_should_i_withdraw_amount
* should_i_withdraw_amount
  - action_fetch_portfolio
  - slot{"portfolio_query":"followed","name":"Benjamin Parker"}
  - action_should_i_unfollow_advice
* should_i_withdraw_amount
  - action_fetch_portfolio
  - slot{"portfolio_query":"followed","name":"Kanya Bunnag"}
  - action_should_i_unfollow_advice
  - action_reset_slots

## should_i_withdraw_amount_should_i_follow
* should_i_withdraw_amount
  - action_fetch_portfolio
  - slot{"portfolio_query":"followed","name":"Alois Reiter"}
  - action_should_i_unfollow_advice
* should_i_follow
  - action_fetch_portfolio
  - slot{"portfolio_query":"not_followed","name":"Masami Nishimura"}
  - action_should_i_unfollow_advice
  - action_reset_slots

## should_i_withdraw_amount_should_i_unfollow
* should_i_withdraw_amount
  - action_fetch_portfolio
  - slot{"portfolio_query":"followed","name":"Florianne Paget"}
  - action_should_i_unfollow_advice
* should_i_unfollow
  - action_fetch_portfolio
  - slot{"portfolio_query":"followed","name":"Masami Nishimura"}
  - action_should_i_unfollow_advice
  - action_reset_slots

## should_i_withdraw_amount_should_i_add_amount
* should_i_withdraw_amount
  - action_fetch_portfolio
  - slot{"portfolio_query":"followed","name":"Paulinho Simoes"}
  - action_should_i_unfollow_advice
* should_i_add_amount
  - action_fetch_portfolio
  - slot{"portfolio_query":"followed","name":"Masami Nishimura"}
  - action_should_i_unfollow_advice
  - action_reset_slots

## should_i_withdraw_amount_invalid
* should_i_add_amount
  - action_fetch_portfolio
  - slot{"portfolio_query":"invalid","name":"Jack"}
  - utter_invalid_portfolio
  - action_reset_slots

## should_i_withdraw_amount_none
* should_i_withdraw_amount
  - action_fetch_portfolio
  - slot{"portfolio_query":null,"name":null}
  - utter_invalid_portfolio
  - action_reset_slots

## should_i_withdraw_amount_followed_with_withdraw_amount_successful
* should_i_withdraw_amount
  - action_fetch_portfolio
  - slot{"portfolio_query":"followed","name":"Benjamin Parker"}
  - action_should_i_unfollow_advice
* withdraw_amount_from_him_her
  - action_withdraw_amount
  - action_reset_slots

## should_i_withdraw_amount_followed_with_withdrawadd_successful
* should_i_withdraw_amount
  - action_fetch_portfolio
  - slot{"portfolio_query":"followed","name":"Kanya Bunnag"}
  - action_should_i_unfollow_advice
* withdraw_from_him_her
  - action_ask_withdraw_amount
  - slot{"portfolio_query":"followed","name":"Kanya Bunnag"}
* amount
  - action_withdraw_amount
  - action_reset_slots

## should_i_withdraw_amount_followed_with_withdraw_successful
* should_i_withdraw_amount
  - action_fetch_portfolio
  - slot{"portfolio_query":"followed","name":"Kanya Bunnag"}
  - action_should_i_unfollow_advice
* do_it
  - action_ask_withdraw_amount
  - slot{"portfolio_query":"followed","name":"Kanya Bunnag"}
* amount
  - action_withdraw_amount
  - action_reset_slots

## should_i_withdraw_amount_followed_with_withdraw_successful
* should_i_withdraw_amount
  - action_fetch_portfolio
  - slot{"portfolio_query":"followed","name":"Kanya Bunnag","amount_query":"valid","amount":"100"}
  - action_should_i_unfollow_advice
* do_it
  - action_withdraw_amount
  - action_reset_slots

## should_i_withdraw_amount_invalid_name
* should_i_withdraw_amount
  - action_fetch_portfolio
  - slot{"portfolio_query":"invalid","name":"George Smith"}
  - utter_invalid_portfolio
  - action_reset_slots

## should_i_withdraw_amount_null_name
* should_i_withdraw_amount
  - action_fetch_portfolio
  - slot{"portfolio_query":null,"name":null}
  - utter_invalid_portfolio
  - action_reset_slots

## should_i_withdraw_amount_invalid_amount
* should_i_withdraw_amount
  - action_fetch_portfolio
  - slot{"amount_query":"invalid","amount":"-48.239"}
  - utter_invalid_amount
  - action_reset_slots
