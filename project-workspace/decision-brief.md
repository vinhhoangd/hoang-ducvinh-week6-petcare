# Decision Brief: Dog daycare with grooming, Warwick town vs Monroe town

**Team 3:** Vinh Hoang (data), Yuhe Luo (research), Shiming Wan (model) · Case 4, Pet-care · Orange County, New York · November 2026

## The decision
The client must decide whether to open a dog daycare with grooming, as the first step toward a full-service pet-care center, in Warwick town or Monroe town, and whether to proceed now or pilot it first.

## Recommendation: **Pilot**
Do not sign a lease in either town yet. Public data cannot show where the pet owners are, and on the one money measure it does have, the two towns cannot be told apart. Run a four-week, low-cost pilot in **both** towns and choose the town by real sign-ups.

## What the evidence says (each claim is a row in `evidence/claim-ledger.csv`)

1. **The two towns' household incomes cannot be ranked.** Warwick town's median household income is $117,680 ± $8,605 (range $109,075–$126,285); Monroe town's is $116,019 ± $13,663 ($102,356–$129,682). The ranges overlap, so the $1,661 difference is within survey error. *(L4, C6 — supported)*

2. **Warwick town has more people, but people are not pet owners.** Warwick has 31,909 residents and Monroe 21,299. A bigger town is a bigger pool of possible customers, but this is only a stand-in for demand. *(L6 — proxy)*

3. **No public dataset counts pet owners or pet spending.** None of the 28,299 variables in the 2023 American Community Survey counts household pets; the 54 animal-related ones are jobs and industries. The AI-written brief's "4,491 pet-owning households in Warwick" has no source and is refuted. Pet demand in each town is **unknown**. *(L3 — supported; C1 — refuted)*

4. **There are 24 pet-care businesses with employees in all of Orange County — not a count of nearby competitors.** County Business Patterns 2022 reports 24 establishments in pet care (except veterinary) for the whole county; it leaves out one-person businesses and gives no town split. The 40 veterinary establishments are a different industry, not direct competitors. *(L1 — supported; C2 — refuted)*

5. **Renting does not separate the towns.** 19.38% of occupied homes in Warwick town are rented (2,276 of 11,743) and 19.01% in Monroe town (1,303 of 6,855). Whether renters buy more or less dog care is unknown. *(C4 — proxy; L7 — supported)*

6. **Pet-food prices rose 1.57% nationally over the latest year — this says nothing about local daycare prices.** The FRED index for pet food and treats (U.S. city average, index points, not dollars) moved from 191.485 (Aug 2025) to 194.485 (Aug 2026). *(C5 — proxy; L2 — supported)*

7. **A prediction model cannot settle it either.** Our best model of neighbourhood income (a random forest on 91 tracts) is off by $16,581 per tract on tracts it had not seen (held-out R² 0.552). That error is ten times the gap between the towns, and Monroe town is only 5 tracts, Warwick 8. *(L8 — supported)*

## Main uncertainty
**How many dog owners in each town would pay for daycare and grooming, and at what price.** No public number measures this. Everything above either cannot rank the towns (claims 1, 5, 7) or is only a stand-in for demand (claims 2, 6).

## Primary research that would reduce it — a four-week pilot
1. **Licensed-dog counts:** ask the Warwick and Monroe town clerks for the number of licensed dogs (dog licences are issued by the town in New York). This is the closest local count of dog owners.
2. **Pre-registration page with a small refundable deposit**, advertised equally in both towns: count sign-ups and deposits per town per week.
3. **One pop-up daycare-and-grooming Saturday in each town:** count bookings, repeat bookings, and the price people accept.
4. **Ten-minute survey of local groomers and boarding businesses** serving each town: waitlists and prices.

**Decision rule after four weeks:** open in the town with clearly more paid deposits and repeat pop-up bookings. If neither town reaches the client's break-even number of regular customers, do not proceed. If the two towns are close, investigate further rather than guess.

## What we checked and what we corrected
Every number above was recomputed from the raw downloads in `data/raw/` and every cited page was opened (Step 8). The AI-written brief we were given recommended "Open in Monroe town. The data clearly supports this choice." That recommendation is refuted: it rested on an invented pet count (C1), on veterinarians counted as groomers' competitors (C2), on national trends read as local spending (C3), and on an income difference that is inside the margin of error (C6).
