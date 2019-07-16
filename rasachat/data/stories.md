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
  - slot{"portfolio_query":"not_followed"}
  - utter_ask_follow_amount
* amount
  - action_follow

## follow
* follow
  - action_fetch_portfolio
  - slot{"portfolio_query":"invalid"}
  - utter_invalid_portfolio

## follow
* follow
  - action_fetch_portfolio
  - slot{"portfolio_query":"followed"}
  - utter_already_followed_portfolio

## unfollow
* unfollow
  - action_fetch_portfolio
  - slot{"portfolio_query":"followed"}
  - action_unfollow

## unfollow
* unfollow
  - action_fetch_portfolio
  - slot{"portfolio_query":"not_followed"}
  - utter_already_not_followed_portfolio

## unfollow
* unfollow
  - action_fetch_portfolio
  - slot{"portfolio_query":"invalid"}
  - utter_invalid_portfolio
