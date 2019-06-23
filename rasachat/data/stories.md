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
  - action_follow

## unfollow
* unfollow
  - action_unfollow
