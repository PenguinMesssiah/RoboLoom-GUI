warp_def = "These threads run lengthwise (vertically) through the cloth. The loom holds these threads under tension while weaving."

weft_def = "These threads run side to side (horizontally) in the cloth. The weft thread is inserted or thrown by the weaver."

weft_face_def = ""
warp_face_def = ""

heddle_def  = "Heddles select the threads the loom raises or lowers to make and opening (shed) for the shuttle to pass through.\
\nIn shaft loom weaving, heddles are connected to the shaft to easily raise pairs of threads for more complex patterns."
shaft_def   = "Shafts are long rodes connected to warp threads through the heddles to raise or lower threads."
shed_def    = "The opening created in the warp when threads are raised or lowered by the heddle."
shuttle_def = "A tool designed to hold and store the weft thread, thrown through the shed while weaving."
float_def   = "When one thread passes over multiple other threads, we call this jump a float because the given thread \
\n \"floats\" on top of the others. Floats allow for weaving structures to be more fluid or flexible.\n\n"

threading_def = "The threading is the horizontal grid at the top of the draft. Each row represents a shaft,\
\nwith the one on the bottom representing the shaft closest to you (shaft #1), and the one on the top,\
\n(shaft #4) the farthest. The columns in the threading draft represent a single end — one thread."

tie_up_def    = "The tie-up is represented by the small square at the upper right of your weaving draft.\
\nThe tie-up is the connection point between your threading draft and the pedals (or levers) you operate while weaving.\
\nThe rows represent the shafts (just like the threading!), and the columns represent your treadles.\
\nWhen you press a treadle, the tie-up tells the loom which shafts rise and which shafts fall \n(depending on the type of loom you have)."

treadling_def = "The treadling is the grid that travels vertically below the tie-up.\
\nThe treadling is the instructions that you\'ll follow when sitting at your loom: \
\neach row represents one pick of weft/one throw of your shuttle, \
\nwhile each column represents a treadle. It is read from the top (closest to the tie-up) down."

drawdown_def = "This is a visual representation of what happens when you are weaving. \
\nIt is positioned under the threading draft and to the left of the treadling. \
\nIt shows what each warp and weft thread is doing during each pick."

cp_info = "We will describe and provide examples of the 3 major basic weaving structure: plain, twill, and satin.\
\nAdditionally, we will highlight two more complex culturally important weaving structures, such as\
\nthe BLANK and kente cloth."

plain_weave_def= "The plain weave is the simplist of all weaving structures.\
\nThis structure consist of equally alternativing the warp & weft threads to create an interlocking pattern."

twill_weave_def= "The twill weave is the second univerally recognized basic weaving structure.\
\nThis structure is denoted with the notation (U x O) twill, where the weft thread \
\npassing under U warp threads then over O warp threads.\
\nPlease note the example above depicts a 1x2 twill weave."

satin_weave_def= "The satin weave is the final major basic weaving structure. The satin weave denotes four or more \
\n warp threads passing over or floating above a weft thread. Similar to the twill weave, \
\nthis structure can be denoted by (U x O) satin. Please note the example above depicts\
\na 4x1 weft-facing satin weave."

satin_weave_cul="The origins of the satin weave date back to medivial China. However, some scholars contend silk and\
\nsatin weaving techniques predate 4000 to 3000 B.C. in mainland China. Historically, satin weaving was performed\
\nexclusively with silk, exported along the Silk Road, from the port city of Quanzhou, and worn by the emperor or\
\nhigh-ranking nobility. Now this timeless technique can be enjoyed by people from all walks of life."

linAlg_info = "We will provide a basic overview of the linear algebra concepts needed to understand the math behind weaving.\
\nThis review will briefly discuss vectors, vector notation, along with vector and matrix operations."

vector_def= "In the simpliest form, vectors are a pair, or set, of numbers/symbols that represent a value or set of values.\
\nThese values can be purely abstract or relate to any user defined data such as a set of geometric coordinates\
\nor linear equations. In our application, we will use vectors to represent a matrix.\
\nTraditionally, vectors are denoted in row column format. This means we classify a vector's size or dimension \
\nby the number of rows present, r, and the number of columns, c, shown below."

vector_ops_add= "Vector addition consists of adding the corresponding elements within each vector.\
\nWe identify corresponding elements by matching these subitems based on their respective position in the overall vector.\
\nPlease note you cannot mathematically add vectors of differing sizes or dimensions."

vector_ops_scalar= "Scalar multiplication denotes multiplying the entire vector by a singular constant value.\
\nTo perform scalar multiplication, multiply every single element in the vector with the defined constant."

matrix_def="We define a matrix as a rectangular array of numbers, denoted by any symbol such as A. Similarly, \
\na matrix can be defined as a collection of vectors. Similar to vectors, matracies sizes are defined \
\nin row column format. For example, when A has m rows and n columns, it is an \"m by n\" matrix. \
\nWe will use matracies to convert the separate components of the weaving draft into solvable mathematic operations."

matrix_ops="The rules for matrix operations follow closely with those of vector operations.\
\n1. Matracies can be added if their shapes are the same.\
\n2. They can be multiplied by any scalar value.\
\n3. To multiply two matracies A*B, traditionally written as AB: If A has n columns, B must have n rows.\
\na. The entry in row i and column j of AB is (row i of A) * (column j of B)\
\n\nExample:"

kente_def = "The kente cloth is a complex woven structure orginating from West Africa. In order to weave a single square\
\npattern (shown below), please follow the provided weaving draft."
kente_instruct= "Please note this structure requires multiple yarn colors for both the warp and weft threads.\
\nSpecifically, the example requires red, green, and yellow yarn for the warp threads along with\
\nseparate black and yellow weft threads, indicated by the colored row and column, respectively."


kente_cult="The kente cloth originates from the nation of Ghana off the coast of West Africa, stemming from the\
\nAsante people during the seventeenth century. Traditionally, masculine-identifying individuals wore\
\nthese garments over their shoulder whereas women-identifying individuals wore these clothes as two\
\nseparate peices, one as an ankle-length dress along with a sling to carry supplies or a child.\
\nEvery aspect of the cloth communicates a message about the wearer through the colors:\
\nGold = Status/Serenity\nYellow = Fertility\nGreen = Renewal\nBlue = Pure Spirit/Harmony\nRed = Passion\nBlack = Spiritual Awareness\
\n\nThese colors and patterns convey common motifs that reflect Asante worldviews such as\
\nNkum me fie na nkosu me aboten, translating to \"Don\'t Kill my house and then mourn\
\nfor me in public\" which warns against untrustworthly people."
kente_cult_2="In modern day, African-American students dawn the kente cloth for collegiate graduation ceremonies.\
\nThis practice originiates the fist prime minister of independent Ghana, Kwame Nkrumah, who wore\
\na kente when meeting President Eisenhower at the White House in 1958."