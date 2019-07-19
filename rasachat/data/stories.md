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

## give general advice
* ask_general_advice
  - utter_general_advice

## give follow advice
* ask_follow_advice
  - action_give_following_advice

## give unfollow advice
* ask_unfollow_advice
  - action_give_unfollowing_advice

## follow
* follow
  - action_fetch_portfolio
  - slot{"portfolio_query":"not_followed","name":"Aricka Lewis"}
  - utter_ask_follow_amount
* amount
  - action_follow
  - action_reset_slots
  - slot{"portfolio_query":null,"name":null,"amount_query":null,"amount":null}

## follow
* follow
  - action_fetch_portfolio
  - slot{"portfolio_query":"invalid","name":"Jeremy"}
  - utter_invalid_portfolio
  - action_reset_slots
  - slot{"portfolio_query":null,"name":null,"amount_query":null,"amount":null}

## follow
* follow
  - action_fetch_portfolio
  - slot{"portfolio_query":"followed","name":"Alois Reiter"}
  - utter_already_followed_portfolio
  - action_reset_slots
  - slot{"portfolio_query":null,"name":null,"amount_query":null,"amount":null}

## unfollow
* unfollow
  - action_fetch_portfolio
  - slot{"portfolio_query":"followed","name":"Masami Nishimura"}
  - action_unfollow
  - action_reset_slots
  - slot{"portfolio_query":null,"name":null,"amount_query":null,"amount":null}

## unfollow
* unfollow
  - action_fetch_portfolio
  - slot{"portfolio_query":"not_followed","name":"Paulinho Simoes"}
  - utter_already_not_followed_portfolio
  - action_reset_slots
  - slot{"portfolio_query":null,"name":null,"amount_query":null,"amount":null}

## unfollow
* unfollow
  - action_fetch_portfolio
  - slot{"portfolio_query":"invalid","name":"John"}
  - utter_invalid_portfolio
  - action_reset_slots
  - slot{"portfolio_query":null,"name":null,"amount_query":null,"amount":null}

## add_amount
* add_amount
  - action_fetch_portfolio
  - slot{"portfolio_query":"not_followed","name":"Florianne Paget", "amount_query":"valid","amount":"50.00"}
  - action_follow
  - action_reset_slots
  - slot{"portfolio_query":null,"name":null,"amount_query":null,"amount":null}

## add_amount
* add_amount
  - action_fetch_portfolio
  - slot{"portfolio_query":"followed","name":"Ralph Axelsen","amount_query":"valid","amount":"100"}
  - action_add_amount
  - action_reset_slots
  - slot{"portfolio_query":null,"name":null,"amount_query":null,"amount":null}

## add_amount
* add_amount
  - action_fetch_portfolio
  - slot{"portfolio_query":"invalid","name":"shrek"}
  - utter_invalid_portfolio
  - action_reset_slots
  - slot{"portfolio_query":null,"name":null,"amount_query":null,"amount":null}

## add_amount
* add_amount
  - action_fetch_portfolio
  - slot{"amount_query":"invalid","name":"Andrzej Kraviec","amount":"-12.00"}
  - utter_invalid_amount
  - action_reset_slots
  - slot{"portfolio_query":null,"name":null,"amount_query":null,"amount":null}

## withdraw_amount
* withdraw_amount
  - action_fetch_portfolio
  - slot{"portfolio_query":"followed","name":"Alois Reiter","amount_query":"valid","amount":"50"}
  - action_withdraw_amount
  - action_reset_slots

## withdraw_amount
* withdraw_amount
  - action_fetch_portfolio
  - slot{"portfolio_query":"invalid","name":"Mark Ritz","amount_query":"valid","amount":"10.00"}
  - utter_invalid_portfolio
  - action_reset_slots

## withdraw_amount
* withdraw_amount
  - action_fetch_portfolio
  - slot{"portfolio_query":"not_followed","name":"William Shore","amount_query":"valid","amount":"65.50"}
  - utter_already_followed_portfolio
  - action_reset_slots

## withdraw_amount
* withdraw_amount
  - action_fetch_portfolio
  - slot{"portfolio_query":"followed","name":"Kanya Bunnag","amount_query":"invalid","amount":"-80"}
  - utter_invalid_amount
  - action_reset_slots

## unfollow_everyone
* unfollow_everyone
  - utter_are_you_sure_unfollow_everyone
* affirm
  - action_unfollow_everyone

## unfollow_everyone
* unfollow_everyone
  - utter_are_you_sure_unfollow_everyone
* deny
  - utter_okay
