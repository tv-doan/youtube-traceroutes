### Tracing the Path to YouTube − A Quantification of Path Lengths and Latencies towards Content Caches

Trinh Viet Doan, Ljubica Pajevic, Vaibhav Bajpai, Jörg Ott  
Technical University of Munich

IEEE Communications Magazine  

Presented at MAT WG Meeting, RIPE 77, Amsterdam. [Slides &rarr;](http://home.in.tum.de/~doan/2018-ripe77-slides.pdf)

---

### Vantage Points

The dataset is collected from ~100 SamKnows probes:

![](http://i.imgur.com/zVefNfd.png)

### Dataset

The raw dataset is available at:

* [Technical University of Munich, mediaTUM &rarr;](http://doi.org/10.14459/2018md1447027)

It is stored as a sqlite3 database `youtube-may-2016-2018.db`. The schema of the tables can be found under [`./data/youtube-traceroute-schema.sql`](https://github.com/tv-doan/youtube-traceroutes/blob/master/data/youtube-traceroute-schema.sql)).
This repository contains (most of) the required metadata to reproduce the results, see below for further instructions.

### Requirements

To read from the database (see above), `sqlite3` is needed.
The analyses were performed using `jupyter` notebooks on `Python 2.7`.
Required Python dependencies are listed in [`requirements.txt`](https://github.com/tv-doan/youtube-traceroutes/blob/master/requirements.txt) and can be installed using `pip install -r requirements.txt`.

For the calculation of CDFs and drawing of the corresponding plots, [`Pmf.py` &rarr;](http://greenteapress.com/thinkstats/Pmf.py) and [`Cdf.py` &rarr;](http://greenteapress.com/thinkstats/Cdf.py) from [Think Stats &rarr;](https://greenteapress.com/wp/think-stats-2e/) are used.

Further, `as_types.txt` (downloaded from [CAIDA's AS Classification &rarr;](https://www.caida.org/data/as-classification/)) is used to assign certain types to the ASes seen in the traceroute measurements.  

### Repeating the results
Move the required datasets and modules to the right locations:
- `youtube-may-2016-2018.db` &rarr; [`./data/`](https://github.com/tv-doan/youtube-traceroutes/tree/master/data)
- `Pmf.py` &rarr; `.`
- `Cdf.py` &rarr; `.`
- `as_types.txt` &rarr; [`./metadata/`](https://github.com/tv-doan/youtube-traceroutes/tree/master/metadata)

Run the [`nb-create_tables.ipynb`](https://github.com/tv-doan/youtube-traceroutes/blob/master/nb-create_tables.ipynb) notebook to process and aggregate the raw dataset, which will store the results in a separate database. After that, the other notebooks `nb-*.ipynb` can be used to draw the plots presented in the paper.
All plots are saved under [`./plots/`](https://github.com/tv-doan/youtube-traceroutes/tree/master/plots).

Note: the lookup of metadata was already done, however, it can be repeated by running [`./metadata/metadata_lookup.py`](https://github.com/tv-doan/youtube-traceroutes/blob/master/metadata/metadata_lookup.py).

### Further analyses and results
For a previous version of the dataset (covering measurements from 05/2016 until 03/2017), more analyses and results can be found [here &rarr;](https://www.cm.in.tum.de/fileadmin/w00bvd/www/thesis/mt-doan.pdf).


### Contact

Please feel welcome to contact the authors for further details.

- Trinh Viet Doan (<doan@in.tum.de>)
- Ljubica Pajevic (<kaerkkal@in.tum.de>)
- Vaibhav Bajpai (<bajpaiv@in.tum.de>)
- Jörg Ott (<ott@in.tum.de>)
