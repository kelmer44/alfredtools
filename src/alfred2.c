#include <stdio.h>
#include <stdlib.h>

int index2=0;
unsigned char *pic;

void saveAnim(unsigned char *bufferFile, int indexCab, unsigned int offset, char extra)
{

	int w=bufferFile[0];
	int h=bufferFile[1];
	int n=bufferFile[4];

	if ((w==0) || (h==0) || (n==0))
		return;
	else
	{

		// QImage *image=new QImage(w*n,h,QImage::Format_Indexed8);


		// int p=indexCab/55;
		// int p2=(p*13)+11;
		// memset(bufpal,0,3);
		// itoa(p2,bufpal,10);

		// memcpy(&paleta[69],&bufpal[0],3);

		// FILE *fp2=fopen(paleta,"rb");
		// unsigned char *bufferPaleta=(unsigned char *)malloc(768);
		// fread(bufferPaleta, 1, 768, fp2);
		// fclose(fp2);

		// ctable=new QVector<QRgb>;

		// unsigned int c, a,r,g,b;
		// for(int i = 0; i < 256; ++i)
		// {
		// 	a=0xFF000000;
		// 	r=bufferPaleta[i*3] *2;
		// 	g=bufferPaleta[(i*3) + 1] *2;
		// 	b=bufferPaleta[(i*3) + 2] *2;
		// 	c=a | (r<<16) | (g<<8) | b;
		// 	ctable->append(c);
		// }

		// image->setColorCount(256);
		// image->setColorTable(*ctable);

		// memset(bufpan,0,3);
		// itoa(p,bufpan,10);

		// bool kk;
		// int index3=0;
		// unsigned int superancho,frame,sx,sy,total;
		// total=w*h;
		// superancho=w*n;
		// for (int y=0;y<h;y++)
		// {
		// 	for (int x=0;x<superancho;x++)
		// 	{
		// 		frame=x/w;
		// 		sy=y;
		// 		sx=x-(frame*w);
		// 		image->setPixel(x,y,pic[offset+(frame*total)+(sy*w)+sx]);
		// 	}
		// }

		// QString pp("C:/proyectos/test2/debug/talking");//.png");
		// pp.append(bufpan);
		// if (extra!=NULL)
		// 	pp.append(extra);

		// pp.append(".png");

		// kk=image->save(pp,"PNG");

	}
}

int main(int argc, char *argv[])
{
    char *name = "../files/alfred.2";
    pic = (unsigned char *)malloc(10000*10000*4);
    FILE *fp1 = fopen(name, "rb");

    fseek(fp1, 0L, SEEK_END);
    int size = ftell(fp1);
    fseek(fp1, 0L, SEEK_SET);

    unsigned char *bufferFile = (unsigned char *)malloc(size);
    fread(bufferFile, 1, size, fp1);

    int indexCab = 0;
    unsigned int index = 0;

    index = bufferFile[indexCab] + (bufferFile[indexCab + 1] * 256);
    while (index == 0)
    {
        indexCab += 55;
        index = bufferFile[indexCab] + (bufferFile[indexCab + 1] * 256);
    }

    while (index < size)
    {

        if ((bufferFile[index] == 'B') && (bufferFile[index + 1] == 'U') && (bufferFile[index + 2] == 'D') && (bufferFile[index + 3] == 'A'))
        {

            saveAnim(&bufferFile[indexCab + 9], indexCab, 0, 'a');
            saveAnim(&bufferFile[indexCab + 21], indexCab, bufferFile[indexCab + 9] * bufferFile[indexCab + 10] * bufferFile[indexCab + 13], 'b');

            memset(pic, 0, 72 * 10000 * 4);

            index2 = 0;
            indexCab += 55;

            index = bufferFile[indexCab] + (bufferFile[indexCab + 1] * 256) + (bufferFile[indexCab + 2] * 65536);
            while (index == 0)
            {
                indexCab += 55;
                index = bufferFile[indexCab] + (bufferFile[indexCab + 1] * 256) + (bufferFile[indexCab + 2] * 65536);
            }
        }
        else
        {
            unsigned char count = bufferFile[index];
            unsigned char color = bufferFile[index + 1];
            int k;
            for (k = index2; k < index2 + count; k++)
                pic[k] = color;

            pic[k] = (unsigned char)color;

            index2 += count;
            index += 2;
        }
    }

    exit(0);
}
