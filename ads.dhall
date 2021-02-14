 {- Function to create a bunch of ads in a json file -}
let makeAd  = \(ad : Text) ->
let subject = "${ad}"
let body    = "${ad} säljes till högstbjudande"
let email   = "foo@bar.com"
let price   =  25500
in { subject, body, email, price }   
in [ makeAd "Snöskoter"
, makeAd "Volvo V70"
, makeAd "Vaz Lada"
, makeAd "Skodia Octavia"
, makeAd "Dacia Duster"
, makeAd "Land Rover"
, makeAd "Willys Jeep"
, makeAd "Suzuki RMZ 450"
, makeAd "Yamaha VMax 1200"
, makeAd "Triumph Sprint RS i955"
]
