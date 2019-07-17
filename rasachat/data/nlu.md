## intent:greet
- hey
- hello
- hi
- good morning
- good evening
- hey there

## intent:goodbye
- bye
- goodbye
- see you around
- see you later

## intent:affirm
- yes
- indeed
- of course
- that sounds good
- correct

## intent:deny
- no
- never
- I don't think so
- don't like that
- no way
- not really

## intent:mood_great
- perfect
- very good
- great
- amazing
- wonderful
- I am feeling very good
- I am great
- I'm good

## intent:mood_unhappy
- sad
- very sad
- unhappy
- bad
- very bad
- awful
- terrible
- not very good
- extremely sad
- so sad

## intent:ask_general_advice
- give me some advice
- what should I do?

## intent:ask_follow_advice
- who should I follow?
- who should I start following?

## intent:ask_unfollow_advice
- who should I unfollow?
- who should I stop following?

## intent:follow
- follow [Andrzej Kraviec](name)
- follow [Masami Nishimura](name)
- start following [William Shore](name)
- start following [Masami Nishimura](name)
- I want to follow [Florianne Paget](name)
- I want to follow [Benjamin Parker](name)
- I would like to follow [Paulinho Simoes](name)
- I would like to follow [William Shore](name)
- I want to start following [Alois Reiter](name)
- I want to start following [Andrzej Kraviec](name)

## intent:add_amount
- put [10.00](CARDINAL) on [Andrzej Kraviec](name)
- put [603](CARDINAL) on [Andrzej Kraviec](name)
- invest [343](CARDINAL) on [Aricka Lewis](name)
- invest [23.54](CARDINAL) on [Alois Reiter](name)
- I want to add [30](CARDINAL) to [Florianne Paget](name)
- I'd like to add [129.72](CARDINAL) to [Paulinho Simoes](name)
- increase [72.80](CARDINAL) on [Benjamin Parker](name)
- increase by [43](CARDINAL) [Benjamin Parker](name)'s portfolio
- add [3](CARDINAL) to [Paulinho Simoes](name)'s portfolio
- add [13.16](CARDINAL) to [Benjamin Parker](name)'s portfolio
- add [50](CARDINAL) to [William Shore](name)
- add another [2.39](CARDINAL) to [Ralph Axelsen](name)
- add another [75](CARDINAL) to [Kanya Bunnag](name)
- I'd like to put [134](CARDINAL) on [William Shore](name)
- I'd like to put [63.24](CARDINAL) on [Florianne Paget](name)
- I want to invest another [200.34](CARDINAL) on [Masami Nishimura](name)
- I want to invest another [12](CARDINAL) on [Ralph Axelsen](name)
- I'd like to increase by [159.16](CARDINAL) [Alois Reiter](name)
- I'd like to increase by [65](CARDINAL) [Kanya Bunnag](name)
- put another [25](CARDINAL) on [Kanya Bunnag](name)
- put another [178.39](CARDINAL) on [Aricka Lewis](name)

## intent:unfollow
- unfollow [Aricka Lewis](name)
- unfollow [Paulinho Simoes](name)
- stop following [Masami Nishimura](name)
- stop following [Florianne Paget](name)
- I want to unfollow [Benjamin Parker](name)
- I want to unfollow [Florianne Paget](name)
- I would like to unfollow [William Shore](name)
- I would like to unfollow [Paulinho Simoes](name)
- I want to stop following [Andrzej Kraviec](name)
- I want to stop following [Alois Reiter](name)

## intent:amount
- [50](CARDINAL)
- [4.00](CARDINAL)
- [100.03](CARDINAL)
- [10.00](CARDINAL)
- [200](CARDINAL)
- [41.32](CARDINAL)
- [2](CARDINAL)
- [73.94](CARDINAL)
- [741.32](CARDINAL)
- [34](CARDINAL)
- [916](CARDINAL)
- [81.79](CARDINAL)
- [150.23](CARDINAL)
- [409](CARDINAL)
- [24.94](CARDINAL)

## lookup:name
- Andrzej Kraviec
- Aricka Lewis
- Benjamin Parker
- Florianne Paget
- Kanya Bunnag
- Masami Nishimura
- Paulinho Simoes
- Ralph Axelsen
- William Shore

## regex:CARDINAL
- ^(\d{1,5}|\d{0,5}\.\d{1,2})$
