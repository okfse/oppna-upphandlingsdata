# Öppna upphandlingsdata (Open Swedish Procurement data)

This project aims at providing open procurement data in the best way possible. It is built on the new [Statistics database of Upphandlingsmyndigheten](https://www.upphandlingsmyndigheten.se/statistik/statistikdatabasen/), which was released last year thanks to the amazing work of Andreas Doherty and his colleagues. This tool already allows anyone to visualise, filter and export data in Excel and CSV. But it can be a cumbersome process as the website isn't very well optimised and the data is broken down in several categories.

This project builds on the same API as the tool and is able to download the data in a quicker way. It also aggregates the data in a way that the online tool doesn't allow (available soon).

## What data is available?

In the ***data*** folder, there are files for each category on the website:

- Antal anbud (*number_of_tenders*)
- Antal kontrakterade anbud (actually contained in the next one)
- Antal kontrakterade anbud\* (*number_of_contracted_tenders_with_suppliers*)
- Antal upphandlingar (*number_of_procurements*, *number_of_innovation, \_environmental\_ and _social_procurements*)
- Kontrakterat värde (*contracted_value*)
- Antal valfrihetssystem (*number_of_valfrihetssystem*)

These files are available in two formats (CSV and Excel) and cleaned to reduce their weight and make them easier to manipulate. For instance, "Direktiv styrd" and "Inte direktivstyrd" are replace by `True` and `False` respectively while "Uppgift saknas" is simply replaced by an empty value.

In addition, the file *all_parameters.json* contains a tree with all the parameters that can be used to query the data.

## License

The data is available as CC0 as it can be considered to be *"allmänna handlingar"* according to the Swedish FOIA (*offentlighetsprincipen*).

The code is available as AGPLv3.
