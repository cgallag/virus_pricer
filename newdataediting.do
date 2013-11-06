gen pctvirus=numvirus/links
gen game=class=="game"
gen anubis=virusscanner=="anubis"
gen vtnew=virusscanner=="vt_new"
gen usenet=downloadsource=="usenet"
gen och=downloadsource=="och"
gen amazon=pricesource=="amazon"
gen pricegame=price*game
gen priceoch=price*och
gen priceusenet=price*usenet
replace avgseverity=avgseverity*10 if anubis==0
