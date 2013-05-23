presidents
==========

Inspired by (and lifting large amounts of code from) Trey Causey's <a href = "http://thespread.us/blog/?p=39">investigation of the language that ESPN uses to discuss white and non-white quarterbacks</a>, I similarly wondered about the language ESPN uses to discuss white and non-white <i>Presidents</i>.  For instance, a common stereotype is that non-white Presidents assassinate their citizens using unmanned drones, while white Presidents assassinate their citizens using polonium-210.  Do such stereotypes creep into sportswriting?

Toward that end, I used <a href = "http://www.scrapy.org/">Scrapy</a> to scrape all the articles from the ESPN website that matched searches for (president obama), (president bush), (president clinton), and so on.  This gave me a total of 543 articles.  Then, using <a href = "https://en.wikipedia.org/wiki/Black_president#Presidents_and_presidential_candidates">Wikipedia</a>, <a href = "https://requester.mturk.com/tour/categorization">Mechanical Turk</a>, and a proprietary <a href = "http://en.wikipedia.org/wiki/Deep_learning">deep learning</a> model, I categorized each of these Presidents as either "white" or "non-white".

Using <a href = "http://nltk.org/">NLTK</a>, I tokenized each article into sentences and then identified each sentence as being about 

<ul> 
<li> one or more white Presidents
<li> one or more non-white Presidents
<li> both white and non-white Presidents
<li> no presidents
</ul>

Curiously, while there were very few "non-white" Presidents, there were nonetheless about <i>four times as many</i> "non-white" sentences as "white" sentences.  (This is itself an interesting phenomenon that's probably worth investigating.)

I then split each sentence into words and counted how many times each word appeared in "white", "non-white", "both", and "none" sentences.  Like Trey, I followed the analysis <a href = "http://nbviewer.ipython.org/5105037">here</a>, similarly excluding stopwords and proper nouns, which I inferred based on capitalization patterns.

Finally, for each word I computed a "white percentage" and "non-white percentage" by looking at how likely that word was to appear in a "white" sentence or a "non-white" sentence and adjusting for the different numbers of sentences.

After all that, here are the words that were most likely to appear in sentences about "white" Presidents:

plaque 5
severed 4
grab 4 
investigation 3
worn 3
unable 3
child 3
suppose 3
block 3
living 3
holders 3
pounds 3
ticket 3
blackout 3
thrown 3
exercise 3
scene 3
televised 3
upon 3
executives 3

Clearly this reads like something out of "CSI" or possibly "CSI: Miami".  If I were to make these words into a story, it would probably be something macabre like

<blockquote>The President <b>grabbed</b> the <b>plaque</b> he'd secretly made from a <b>living</b> <b>child</b>'s <b>severed</b> foot and <b>worn</b> sock.  The <b>investigation</b> <b>supposed</b> a suspect weighing at least 200 <b>pounds</b> who could have <b>thrown</b> the victim down the <b>block</b>, not a feeble politician famous for his <b>televised</b> <b>blackout</b> when he tried to <b>exercise</b> but was <b>unable</b> to <b>grab</b> his toes.</blockquote>

In constrast, here are the words most likely to appear in sentences about "non-white" Presidents:

bracket 32
interview 21
trip 16
champions 16
fan 48 1
asked 35 1
carrier 11
celebrate 11
thinks 11
early 11
eight 11
personal 10
picks 10
appearance 10
far 9
hear 9
congratulating 9
given 9
troops 9
safety 9
fine 9
person 9

This story would have to be something uplifting like

<blockquote>The President promised to raise taxes on every <b>bracket</b> before ending the <b>interview</b>.  As a huge water polo <b>fan</b>, he needed to catch a ride on an aircraft <b>carrier</b> for his <b>trip</b> to <b>celebrate</b> with the <b>champions</b>.  "Sometimes I get <b>asked</b>," he <b>thinks</b>, "whether it's too <b>early</b> to eat a <b>personal</b> pan pizza with <b>eight</b> toppings.  So <b>far</b> I always say that I <b>hear</b> it's not."  His <b>safety</b> is a <b>given</b>, since he's surrounded by <b>troops</b> who are always <b>congratulating</b> him for being a <b>fine</b> <b>person</b> with a <b>fine</b> <b>appearance</b>.</blockquote>

As you can see, it has a markedly different tone, but not in a way that obviously correlates with the stereotypes mentioned earlier.  

Obviously, this is only the tip of the iceberg.  The algorithm for identifying which sentences were about Presidents is pretty rudimentary, and the word-counting NLP techniques used here are pretty basic.  Another obvious next step would be to pull in additional data sources like <a href = "http://sports.yahoo.com/">Yahoo! Sports</a> or <a href = "http://sportsillustrated.cnn.com/">SI.com</a> or <a href = "http://msn.foxsports.com/">FOX Sports</a>.  

If you're interested in following up, the code is all up on my <a href = "https://github.com/joelgrus/presidents">github</a>, so have at it!