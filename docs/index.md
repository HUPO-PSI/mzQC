---
#
# By default, content added below the "---" mark will appear in the home page
# between the top bar and the list of recent posts.
# To change the home page layout, edit the _layouts/home.html file.
# See: https://jekyllrb.com/docs/themes/#overriding-theme-defaults
#
layout: home
---

## Welcome
This is the HUPO-PSI's Quality Control working group homepage. 
One of the major results/products from the group is

{% include highlight.html 
    content="<b>mzQC:</b><br/> Reporting and exchange format for mass spectrometry quality control data from HUPO-PSI"
    icon='&#xf56c;' 
	icon_size='5em' 
	background_color='#ECF7FF' 
	border_color='#0065B4' 
	icon_color='#248031' 
    font_size='1.2em'
%}

### For whom is mzQC?

The format is designed to work as ***handover format*** as well as a ***report format*** and ***archive format*** as well. 
As such, we expect it to greatly benefit researchers to better understand their data and improve experimental protocols, 
instrument operators keeping track of their mass spectrometer statuses, 
and analysts wanting a better insight to the data they analyse.

* If you are unfamiliar with JSON or PSI file formats, or generally because the title speaks to you, we recommend to start with [mzQC for analytical chemists](use-cases/analytical-chemists/)

* If you are familiar with JSON or have an understanding of PSI file formats, are however pressed for time, [mzQC at a glance](use-cases/at-a-glance/) will give you a brief overview of the essentials.

* A in a nutshell exlanation is [here](mzQC-in-a-nutshell/)
* Find out more about the format in general [here](mzQC-intro/)!

### Specification Document
For the technical details on the mzQC format see either the [latest release static version](spec-doc/), or 
[the current google doc version](https://docs.google.com/document/d/132F3MBgDJgtFlXxDZhpJ1oHGbKL8pT6dk9fvL55L5_M/edit?usp=sharing).

### About us
You can read more about the group [here](about/) and [here](https://www.psidev.info/groups/quality-control)!

