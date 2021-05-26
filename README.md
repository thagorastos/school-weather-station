# [weather-3dimagnilas.mysch.gr](http://weather-3dimagnilas.mysch.gr)
Σχολικός μετεωρολογικός σταθμός
![Φωτογραφίες μεταωρολογικού σταθμού](https://github.com/thagorastos/school-weather-station/blob/master/φωτογραφίες-υλικού/photo-collage.jpg)
## Στόχοι

Συναρμολόγηση του Microbit Climate Kit
Επικοινωνία με το Raspberry μέσω UART (https://projects.raspberrypi.org/en/projects/microbit-meteorologist) για μεταφορά μετεορολογικών δεδομένων
Λειτουργία web service στο Raspberry με IoT dashboard ( https://www.instructables.com/id/Build-a-Raspberry-Pi-SUPER-Weather-Station/) και αποστολή δεδομένων στο wundergound.com (https://projects.raspberrypi.org/en/projects/uploading-weather-data-to-weather-underground)

Εγκατάσταση του συστήματος στην ταράτσα του σχολείου μας, διασύνδεση με το τοπικό δίκτυο, εγκατάσταση υπολογιστή-οθόνης σε κοινόχρηστο χώρο που θα δείχνει τις μετρήσεις σε πραγματικό χρόνο, άνοιγμα της υπηρεσίας για δημόσια πρόσβαση στο σχολικό δίκτυο και ένταξη του συστήματος στο αναλυτικό πρόγραμμα του σχολείου (για μαθήματα, μελέτης, γεωγραφίας, μετεωρολογίας, προγραμματισμού).

Στο κομμάτι του hardware οι εκπαιδευόμενοι θα κληθούν να μελετήσουν τον τρόπο λειτουργίας μετεωρολογικών οργάνων, να τα διασυνδέσουν (στο microbit), ενώ στο κομμάτι του software θα έρθουν σε επαφή με το θέμα διασύνδεσης των συσκευών microbit με raspberry και των δικτυακών υπηρεσιών με τρόπο προσαρμοσμένο στο επίπεδο που μπορούν να τα κατανοούν. Κοινώς, το δύσκολο-τεχνικό κομμάτι του έργου θα το προσεγγίσουν ως μαύρο κουτί.

## Σχεδιάγραμμα εγκατάστασης υλικού και διασύνδεσης με λογισμικά
![Σχεδιάγραμμα εγκατάστασης υλικού και διασύνδεσης με λογισμικά](https://github.com/thagorastos/school-weather-station/blob/master/meteo.png)

## Υλικό μετεωρολογικού σταθμού

Για τη λήψη μετεωρολογικών δεδομένων χρησιμοποιείται το [Sparkfun Weather kit](http://sparkfun.com/products/16274). Τα εξωτερικά μετεωρολογικά όργανα του κιτ είναι συνδεμένα με το [weatherbit](https://www.sparkfun.com/products/15837), το οποίο τοποθετήθηκε μέσα σε [μετεωρολογικό κλωβό](https://el.wikipedia.org/wiki/Μετεωρολογικός_κλωβός) και είναι συνδεμένο με ένα [microbit](https://en.wikipedia.org/wiki/Micro_Bit).

Οι μετρήσεις μεταφέρονται με καλώδιο USB από τον μετεωρολογικό κλωβό σε στεγανό ηλεκτρολογικό κουτί, μέσα στο οποίο βρίσκεται μονάδα UPS και μονάδα Raspberri Pi.

## Λογισμικό μετεωρολογικού σταθμού

### Λογισμικό για το weatherbit

Ο μετεωρολογικός σταθμός βασίζεται σε προσαρμοσμένο λογισμικό που έχει προγραμαμτιστεί στο περιβάλλον [makecode.microbit.org](http://makecode.microbit.org), έχει εγκατασταθεί στο microbit+weatherbit το οποίο αναλαμβάνει τον μετασχηματισμό δεδομένων στο μετρικό σύστημα και την σειριοποίησή ώστε να αποστέλλεται κάθε 2'' μέσω της σειριακής θύρας. Στο παρόν αποθετήριο, διατηρούνται διάφορες εκδόσεις του λογισμικού (https://github.com/thagorastos/school-weather-station/tree/master/microbit-programs) και χρησιμοποιείται η πιο πρόσφατη (από αυτή εξαρτάται ο οδηγός του weewx).

### Λογισμικό για το raspberry pi

Την κεντρική διαχείριση των μετεωρολογικών δεδομένων αναλαμβάνει το λογισμικό διαχείρισης μετεωρολογικών δεδομένων ανοικτού κώδικα [WeeWX](https://github.com/weewx/weewx). Η διασύνδεση του microbit+weatherbit με το WeeWX γίνεται μέσω καλωδίου USB-σειριακής σύνδεσης από το microbit προς το Raspberry Pi (δεν παίζει ρόλο η θύρα USB που θα χρησιμοποιηθεί) και η εισαγωγή δεδομένων από το microbit γίνεται μέσω προσαρμοσμένου οδηγού (weewx driver) που έχει γραφτεί για το λογισμικό WeeWX. Να σημειωθεί πως οι εκδόσεις του οδηγού microbit.py για το WeeWx και του λογισμικού για το weatherbit πρέπει να είναι συμβατές μεταξύ τους, καθότι βάση αυτών γίνεται η εισαγωγή δεδομένων στο λογισμικό WeeWx.

Το weewx-skin που έχει επιλεγεί είναι το [BelcherTown](https://github.com/poblabs/weewx-belchertown). Για λόγους ευκολίας, στο παρόν αποθετήριο έχει προστεθεί το βασικό αρχείο ρυθμίσεων [weewx.conf](https://github.com/thagorastos/school-weather-station/blob/master/weewx.conf) του WeeWx που περιέχει επίσης override values για το skin.

#### Αρχείο ρυθμίσεων weewx.conf

Για τη λειτουργία του weewx χρειάζεται να προσαρμοστούν οι ρυθμίσεις σας για τις παρακάτω ενότητες:
* mqtt server (για την αποστολή μετρήσεων πραγματικού χρόνου)
* στοιχεία σύνδεσης για ftp ή/και rsync (για την ανάρτηση του περιεχομένου του ιστότοπου)
* API κλειδιά και διαπιστευτήρια για κάθε 3η υπηρεσία διασύνδεσης (π.χ. Windy, Wunderground κ.λπ.)

##### Mosquitto MQTT server

Για την παροχή δεδομένων πραγματικού χρόνου στον ιστότοπο του μετεωρολογικού σταθμού χρησιμοποιείται το λογισμικό Mosquitto MQTT server στο οποίο η δημοσίευση των δεδομένων γίνεται από το λογισμικό WeeWx, έχει ρυθμιστεί mqtt bridge για την διαδίβασή τους σε εικονική μηχανή στο Νέφος-ΠΣΔ σε δεύτερο Mosquitto MQTT σέρβερ και κάθε χρήστης (client) συνδέεται και λαμβάνει δεδομένα μέσω web sockets από τον 2ο mqtt σέρβερ. Η κίνηση αυτή έγινε για λόγους διαχείρισης υπολογιστκών και δικτυακών πόρων.

# Ιστότοπος μετεωρολογικού σταθμού
http://weather-3dimagnilas.mysch.gr/



> Open this page at [https://thagorastos.github.io/school-weather-station/](https://thagorastos.github.io/school-weather-station/)

## Use as Extension

This repository can be added as an **extension** in MakeCode.

* open [https://makecode.microbit.org/](https://makecode.microbit.org/)
* click on **New Project**
* click on **Extensions** under the gearwheel menu
* search for **https://github.com/thagorastos/school-weather-station** and import

## Edit this project ![Build status badge](https://github.com/thagorastos/school-weather-station/workflows/MakeCode/badge.svg)

To edit this repository in MakeCode.

* open [https://makecode.microbit.org/](https://makecode.microbit.org/)
* click on **Import** then click on **Import URL**
* paste **https://github.com/thagorastos/school-weather-station** and click import

## Blocks preview

This image shows the blocks code from the last commit in master.
This image may take a few minutes to refresh.

![A rendered view of the blocks](https://github.com/thagorastos/school-weather-station/raw/master/.github/makecode/blocks.png)

#### Metadata (used for search, rendering)

* for PXT/microbit
<script src="https://makecode.com/gh-pages-embed.js"></script><script>makeCodeRender("{{ site.makecode.home_url }}", "{{ site.github.owner_name }}/{{ site.github.repository_name }}");</script>
