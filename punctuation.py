import string
import math
import sys
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw


## Establish punctuation
def getPunctuation(s):
   include = set(string.punctuation)
   return ''.join(ch for ch in s if ch in include)

def get_punctuation_from_book(bookname):
   print("Getting punctuation.")

   # Get text and punctuation from book
   file = open('books/' + bookname + '.txt','r')
   txt = file.read()
   file.close()

   punct = getPunctuation(txt);

   # Save punctuation to a file
   file = open(bookname + '-punct.txt','w')
   file.write(punct)
   file.close()

   return punct

## Initialize image info
def create_image(punct, bookname):
   print("Creating image.")

   # size of output canvas in pixels
   canvasHeight = 10000;
   canvasWidth = 8000;

   # pixel border width
   trim = 100;

   font1size = 48;
   font2size = 72;

   # number of symbols to be output on each line
   symbolsPerLine = 106;
   # and the number of lines
   linesOfText = 133;

   deltaW = (canvasWidth - trim*2)/symbolsPerLine
   deltaH = (canvasHeight - trim*2)/linesOfText

   bkgColor = (238,212,187)
   bkgColor = (255,255,255)

   # symbolsPerLine = int(math.floor(math.sqrt(len(punct))));
   # linesOfText = int(math.floor(len(punct)/symbolsPerLine));

   img = Image.new("RGB", [canvasWidth,canvasHeight], bkgColor)
   draw = ImageDraw.Draw(img)
   # font from (SEE LICENSE!): http://www.fontsquirrel.com/fonts/glacial-indifference
   font1 = ImageFont.truetype("GlacialIndifference-Bold.otf", font1size)
   font2 = ImageFont.truetype("GlacialIndifference-Bold.otf", font2size)

   # transitionFill = (0,0,0);
   # endSentenceFill = (125,0,0);
   # parentheticalFill = (235,235,235);

   # in case you want to change by transition
   transitionFill = (0,0,0);
   endSentenceFill = (0,0,0);
   parentheticalFill = (0,0,0);

   pages = round(len(punct)/(symbolsPerLine*linesOfText))

   # getTextSize
   symb_count = 0
   for p in range(pages):
      for ii in range(linesOfText):
         for jj in range(symbolsPerLine):
            symb = punct[(jj + ii*symbolsPerLine) + (p*((linesOfText*symbolsPerLine)-1))]
            if (symb == '.'):
               draw.text(
                  (trim + jj*deltaW, trim + ii*deltaH - round(font1size/4)), 
                  symb,
                  fill=endSentenceFill,
                  font=font1)
            elif (symb == ','):
               draw.text(
                  (trim + jj*deltaW, trim + ii*deltaH - round(font1size/4)), 
                  symb,
                  fill=transitionFill,
                  font=font1)
            elif (symb == '!') or (symb == '?'):
               draw.text(
                  (trim + jj*deltaW, trim + ii*deltaH), 
                  symb,
                  fill=endSentenceFill,
                  font=font1)
            elif (symb == '"') or (symb == '\'') or (symb == '(') or (symb == ')') or (symb == '[') or (symb == ']'):
               draw.text(
                  (trim + jj*deltaW, trim + ii*deltaH), 
                  symb,
                  fill=parentheticalFill,
                  font=font1)
            elif (symb == ';') or (symb == '-') or (symb == ':'):
               draw.text(
                  (trim + jj*deltaW, trim + ii*deltaH), 
                  symb,
                  fill=transitionFill,
                  font=font1)
            else:
               draw.text(
                  (trim + jj*deltaW, trim + ii*deltaH), 
                  symb,
                  fill="green",
                  font=font1)
            
            symb_count += 1
            
            if symb_count >= len(punct):
               img.save('images/{}-{}-of-{}.png'.format(bookname, p+1, pages))
               return
      
      img.save('images/{}-{}-of-{}.png'.format(bookname, p+1, pages))
   
      img = Image.new("RGB", [canvasWidth,canvasHeight], bkgColor)
      draw = ImageDraw.Draw(img)

   print("Printed {} total characters.".format(symb_count))

if __name__ == "__main__":
   # Get book name from sys args
   if (len(sys.argv) > 1):
      book = sys.argv[1]
   else:
      book = 'ulysses'

   punct = get_punctuation_from_book(book)
   create_image(punct, book)
   print(len(punct))