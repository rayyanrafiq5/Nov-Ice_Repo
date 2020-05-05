# Nov-Ice_Repo
Libraries Used are Requests,lxml
elements and attributes from html are been extracted using xpath

captcha handeling (my (get_capatch) method)
captcha code is written in such a way that it gets the dynamic url every time a post request is sent,
the image url is requested and the byte tesponse will be written in a .jpeg file and the captcha can be view and entered in the input

all the elements are extracted and made in a list format ,which is later converterted into a dict and later into a json format

error handelling
when the user enter either if the elements which is not valid then the program handels th error and display the apporopriate message
