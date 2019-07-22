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
  - utter_did_that_help
* affirm
  - utter_happy

## sad path 2
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* deny
  - utter_goodbye

## say goodbye
* goodbye
  - utter_goodbye

## give_general_advice
* ask_general_advice
  - utter_general_advice

## give_follow_advice
* ask_follow_advice
  - action_give_following_advice
  - slot{"name":"Alois Reiter"}
  - action_reset_slots

## give_follow_advice_with_follow
* ask_follow_advice
  - action_give_following_advice
  - slot{"name":"Andrzej Kraviec"}
* follow_him_her
  - action_ask_follow_amount
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

## give_unfollow_advice
* ask_unfollow_advice
  - action_give_unfollowing_advice
  - slot{"name":"Aricka Lewis"}
  - action_reset_slots

## give_unfollow_advice_with_unfollow
* ask_unfollow_advice
  - action_give_unfollowing_advice
  - slot{"name":"Aricka Lewis"}
* unfollow_him_her
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
  - action_ask_follow_amount
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
  - slot{"portfolio_query":"not_followed","name":"Florianne Paget", "amount_query":"valid","amount":"50.00"}
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

## withdraw_amount_null_amount
* withdraw_amount
  - action_fetch_portfolio
  - slot{"portfolio_query":"followed","name":"Ralph Axelsen","amount_query":null,"amount":null}
  - utter_invalid_amount
  - action_reset_slots

## withdraw_amount_not_followed
* withdraw_amount
  - action_fetch_portfolio
  - slot{"portfolio_query":"not_followed","name":"William Shore","amount_query":"valid","amount":"65.50"}
  - utter_already_followed_portfolio
  - action_reset_slots

## unfollow_everyone_affirmed
* unfollow_everyone
  - utter_are_you_sure_unfollow_everyone
* affirm
  - action_unfollow_everyone

## unfollow_everyone_denied
* unfollow_everyone
  - utter_are_you_sure_unfollow_everyone
* deny
  - utter_okay

## follow_everyone
* follow_everyone
  - utter_please_follow_one_portfolio_at_a_time

## should_i_follow_followed
* should_i_follow
  - action_fetch_portfolio
  - slot{"portfolio_query":"followed","name":"Florianne Paget"}
  - action_should_i_follow_advice
  - action_reset_slots

## should_i_follow_not_followed
* should_i_follow
  - action_fetch_portfolio
  - slot{"portfolio_query":"not_followed","name":"Benjamin Parker"}
  - action_should_i_follow_advice
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
  - action_ask_follow_amount
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

## should_i_follow_with_unfollow_successful
* should_i_follow
  - action_fetch_portfolio
  - slot{"portfolio_query":"followed","name":"Andrzej Kraviec"}
  - action_should_i_follow_advice
* unfollow_him_her
  - action_unfollow
  - action_reset_slots

## should_i_follow_with_unfollow_already_not_followed
* should_i_follow
  - action_fetch_portfolio
  - slot{"portfolio_query":"not_followed","name":"Andrzej Kraviec"}
  - action_should_i_follow_advice
* unfollow_him_her
  - utter_already_not_followed_portfolio
  - action_reset_slots

## should_i_follow_followed_with_add_amount
* should_i_follow
  - action_fetch_portfolio
  - slot{"portfolio_query":"followed","name":"Ralph Axelsen"}
  - action_should_i_follow_advice
* add_amount_to_him_her
  - action_add_amount
  - action_reset_slots

## should_i_follow_not_followed_with_add_amount
* should_i_follow
  - action_fetch_portfolio
  - slot{"portfolio_query":"not_followed","name":"Masami Nishimura"}
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

## should_i_follow_with_withdraw_amount_not_followed
* should_i_follow
  - action_fetch_portfolio
  - slot{"portfolio_query":"not_followed","name":"Florianne Paget"}
  - action_should_i_follow_advice
* withdraw_amount_from_him_her
  - utter_already_not_followed_portfolio
  - action_reset_slots

## should_i_unfollow_followed
* should_i_unfollow
  - action_fetch_portfolio
  - slot{"portfolio_query":"followed","name":"Kanya Bunnag"}
  - action_should_i_unfollow_advice
  - action_reset_slots

## should_i_unfollow_not_followed
* should_i_unfollow
  - action_fetch_portfolio
  - slot{"portfolio_query":"not_followed","name":"Alois Reiter"}
  - utter_already_not_followed_portfolio
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
