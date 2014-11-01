#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <strings.h>
#include <string.h>

#define	APOS	0
#define	POS1	1
#define	POS2	2
#define	POS3	3

#define	MLET	7

long alphaB[256];

int read_data(char *fNam,int MxCnt,int MxLgh,int MxPos,unsigned char ***data);
void buildAlphabet(char **strs,int cnt,int lgh);
void dump_data(unsigned char **data,char *fName,int cnt);
int maxPos(int p1,int p2,int p3);
int get_type(int cP1,int cP2,int cP3,int iP1,int iP2,int iP3);
int get_line_count(char *fName);
void init_hits(int **hits,int Mx);
void dump_hits(int *hits,unsigned char **cs,int Mx);
void buildHash(int mType);
void match_items_cs(int mType);
void scan_items_type1();
void scan_items_type2();
void scan_items_type3();
void scan_items_typeA();
void buildIndex(long **cIdx,unsigned char **cs,int cCnt,int mType,int cP1,int cP2,int cP3);

char *itemFileName,*cFileName;
int itemCnt=0,cCnt=0;
int cMxCnt,cMxLgh;
int iP1,iP2,iP3;
int cP1,cP2,cP3;
int mType,cLGH=0;
int nPos;
long MxAlpha,mxpos[MLET];
unsigned char **items,**cs;
unsigned char *itemsX,*csX;

int *hits;
long *cIdx;

int *hashCnt,**hash;

int main(int argc,char **argv)
{
		if (argc != 9) {
			fprintf(stderr,"usage: %s <ITEMS> <CS> <p1> <p2> <p3> <p1> <p2> <p3>\n",argv[0]);exit(1);
		}

		itemFileName=argv[1];
		cFileName=argv[2];
		iP1=atoi(argv[3]);
		iP2=atoi(argv[4]);
		iP3=atoi(argv[5]);
		cP1=atoi(argv[6]);
		cP2=atoi(argv[7]);
		cP3=atoi(argv[8]);

		if (iP1 != -1) iP1--;
		if (iP2 != -1) iP2--;
		if (iP3 != -1) iP3--;
		if (cP1 != -1) cP1--;
		if (cP2 != -1) cP2--;
		if (cP3 != -1) cP3--;

		mType=get_type(cP1,cP2,cP3,iP1,iP2,iP3);
		//printf("mType=%d\n",mType);

		cMxCnt=get_line_count(cFileName); 	// needed to allocate memory
		cMxLgh=8; 				// for now, just to allocate memory and read the items
		cCnt=read_data(cFileName,cMxCnt,cMxLgh,maxPos(cP1,cP2,cP3),&cs); // read C items
		cMxLgh=strlen(cs[0]);			// assume all C items are same length

		buildAlphabet(cs,cCnt,cMxLgh);		// assign unique serial number to each letter used in C items

		buildIndex(&cIdx,cs,cCnt,mType,cP1,cP2,cP3); // calculate an index for each C items (unique at up to MLET letters)

		buildHash(mType);			// build hash table with C items

		init_hits(&hits,cCnt);

fprintf(stderr,"prep done\n");

		match_items_cs(mType);			// match GIGA file data to C items using hash table

		dump_hits(hits,cs,cCnt);
}

void buildIndex(long **cIdx,unsigned char **cs,int cCnt,int mType,int cP1,int cP2,int cP3)
{
	int i,j;
	long idx;

	if (((*cIdx) = (long *) malloc(sizeof(long)*cCnt))==0) {
		perror("malloc 1");exit(1);
	}
	switch (mType) {
	case POS1:
		for (i=0;i<cCnt;i++) (*cIdx)[i]=alphaB[cs[i][cP1]];
		break;
	case POS2:
		for (i=0;i<cCnt;i++) (*cIdx)[i]=alphaB[cs[i][cP1]]*MxAlpha + alphaB[cs[i][cP2]];
		break;
	case POS3:
		for (i=0;i<cCnt;i++) (*cIdx)[i]=alphaB[cs[i][cP1]]*MxAlpha*MxAlpha + alphaB[cs[i][cP2]]*MxAlpha + alphaB[cs[i][cP3]];
		break;
	case APOS:
		for (i=0;i<cCnt;i++) {
			for (idx=0,j=0;j<nPos;j++) idx+=mxpos[j]*alphaB[cs[i][j]];
			(*cIdx)[i]=idx;
		}
		break;
	}
}

void buildAlphabet(char **strs,int cnt,int lgh)
{
	int i,j,TooBig;

	for (i=0;i<256;i++) alphaB[i]=0;

	for (i=0;i<cnt;i++) {
		for (j=0;j<lgh;j++) {
			alphaB[strs[i][j]]=1;
		}
	}

	for (j=1,i=0;i<256;i++) {
		if (alphaB[i]) alphaB[i]=j++;
	}
	MxAlpha=j;

	//for (i=0;i<256;i++) if (alphaB[i]) printf("%c=%d\n",i,alphaB[i]);

	// use MxAlpha cMxLgh to decide how to handle APOS cases
	// up to 7 letters on alphabets of size 40 can hold in 32GB
	// for APOS can use 4 to 6 letters without issues
	// use cMxLgh for number of letters to use to build index and hash

	nPos=(cMxLgh>MLET?MLET:cMxLgh); // maximum number of letters we can use to fit in 36GB
	for (TooBig=1;TooBig;) {
		for (i=0;i<nPos;i++) {
			mxpos[i]=1;
			for (j=0;j<i;j++) mxpos[i]*=MxAlpha;
		}
		if (mxpos[nPos-1]*MxAlpha < 1800000000) {
			TooBig=0;
		} else {
			nPos--;
		}
	}
}

void buildHash(int mType)
{
	int i;
	long id,mx;

	switch (mType) {
	case POS1:
		mx=MxAlpha;
		break;
	case POS2:
		mx=MxAlpha*MxAlpha;
		break;
	case POS3:
		mx=MxAlpha*MxAlpha*MxAlpha;
		break;
	case APOS:
		mx=MxAlpha*mxpos[nPos-1];
		break;
	}

	if ((hash=(int **) malloc(sizeof(int *)*mx))==0) {
		perror("malloc 2");exit(1);
	}
	for (i=0;i<mx;i++) hash[i]=0;

	if ((hashCnt=(int *) malloc(sizeof(int)*mx))==0) {
		perror("malloc 3");exit(1);
	}
	for (i=0;i<mx;i++) hashCnt[i]=0;

	for (i=0;i<cCnt;i++) {
		id=cIdx[i];
		if (id>=mx) {
			printf("overflow index error\n");exit(1);
		}
		if ((hash[id]=realloc(hash[id],sizeof(int *)*hashCnt[id]))==0) {
			perror("realloc");exit(1);
		}
		hash[id][hashCnt[id]]=i;
		hashCnt[id]++;
	}
}

void match_items_cs(int mType)
{
	switch (mType) {
	case POS1:
		scan_items_type1();
		break;
	case POS2:
		scan_items_type2();
		break;
	case POS3:
		scan_items_type3();
		break;
	case APOS:
		scan_items_typeA();
		break;
	}
}

void scan_items_type1()
{
	FILE *fil;
	unsigned char dummy,lin[128];
	int i;
	long i1,id;

	if ((fil=fopen(itemFileName,"r"))==0) {
		perror("open");exit(1);
	}

	while (fscanf(fil,"%[^\n]",lin)==1) {
		fscanf(fil,"%c",&dummy);
		if (strcmp(lin,"DATELINE")==0 || strcmp(lin,"HEADLINE")==0) continue;
		if (lin[iP1]==' ') continue;
		//printf("lin=%s\n",lin);
		i1=alphaB[lin[iP1]];
		if (i1==0) continue; // letter will not match with any "C" items
		id=i1;
		for (i=0;i<hashCnt[id];i++) hits[hash[id][i]]++;
	}

	fclose(fil);
}

void scan_items_type2()
{
	FILE *fil;
	unsigned char dummy,lin[128];
	int i;
	long i1,i2,id,m2;

	m2=MxAlpha;

	if ((fil=fopen(itemFileName,"r"))==0) {
		perror("open");exit(1);
	}

	while (fscanf(fil,"%[^\n]",lin)==1) {
		fscanf(fil,"%c",&dummy);
		if (strcmp(lin,"DATELINE")==0 || strcmp(lin,"HEADLINE")==0) continue;
		for (i=iP1;lin[i]!=' ' && i<=iP2;i++);
		if (i<=iP2) continue;
		//printf("lin=%s\n",lin);
		i1=alphaB[lin[iP1]]; i2=alphaB[lin[iP2]];
		if (i1==0 || i2==0) continue; // letter will not match with any "C" items
		id=i1*m2+i2;
		for (i=0;i<hashCnt[id];i++) hits[hash[id][i]]++;
	}

	fclose(fil);
}

void scan_items_type3()
{
	FILE *fil;
	unsigned char dummy,lin[128];
	int i;
	long i1,i2,i3,id,m2,m3;

	m2=MxAlpha;
	m3=MxAlpha*MxAlpha;

	if ((fil=fopen(itemFileName,"r"))==0) {
		perror("open");exit(1);
	}

	while (fscanf(fil,"%[^\n]",lin)==1) {
		fscanf(fil,"%c",&dummy);
		if (strcmp(lin,"DATELINE")==0 || strcmp(lin,"HEADLINE")==0) continue;
		for (i=iP1;lin[i]!=' ' && i<=iP3;i++);
		if (i<=iP3) continue;
		//printf("lin=%s\n",lin);
		i1=alphaB[lin[iP1]]; i2=alphaB[lin[iP2]]; i3=alphaB[lin[iP3]];
		if (i1==0 || i2==0 || i3==0) continue; // letter will not match with any "C" items
		id=i1*m3+i2*m2+i3;
		for (i=0;i<hashCnt[id];i++) hits[hash[id][i]]++;
	}

	fclose(fil);
}

void scan_items_typeA()
{
	FILE *fil;
	unsigned char dummy,lin[128];
	int i,rem;
	long id;

	if ((fil=fopen(itemFileName,"r"))==0) {
		perror("open");exit(1);
	}

	if (nPos==cMxLgh) {
		// letters <= MLET positions so matching index confirms all letters are same
		while (fscanf(fil,"%[^\n]",lin)==1) {
			fscanf(fil,"%c",&dummy);
			if (strcmp(lin,"DATELINE")==0 || strcmp(lin,"HEADLINE")==0) continue;
			for (i=0;lin[i]!=' ' && i<cMxLgh;i++);
			if (i<cMxLgh) continue;
			//printf("lin=%s\n",lin);
			for (i=0;i<nPos;i++) if (alphaB[lin[i]]==0) continue;
			for (id=0,i=0;i<nPos;i++) id+=alphaB[lin[i]]*mxpos[i];
			for (i=0;i<hashCnt[id];i++) {
				hits[hash[id][i]]++;
			}
		}
	} else {
		// letters > MLET positions so must use strncmp to ensure ALL letters match
		rem=cLGH-nPos;
		while (fscanf(fil,"%[^\n]",lin)==1) {
			fscanf(fil,"%c",&dummy);
			if (strcmp(lin,"DATELINE")==0 || strcmp(lin,"HEADLINE")==0) continue;
			for (i=0;lin[i]!=' ' && i<cMxLgh;i++);
			if (i<cMxLgh) continue;
			//printf("lin=%s\n",lin);
			for (i=0;i<nPos;i++) if (alphaB[lin[i]]==0) continue;
			for (id=0,i=0;i<nPos;i++) id+=alphaB[lin[i]]*mxpos[i];
			for (i=0;i<hashCnt[id];i++) {
				// the first nPos letters are a match, so no need to compare
				//if (strncmp(cs[hash[id][i]],lin,cLGH)==0) {
				if (strncmp(&cs[hash[id][i]][nPos],&lin[nPos],rem)==0) {
					hits[hash[id][i]]++;
				}
			}
		}
	}

	fclose(fil);
}

void dump_hits(int *hits,unsigned char **cs,int Mx)
{
	int i;

	for (i=0;i<Mx;i++) {
		if (hits[i]>0) {
			printf("%s,%d\n",cs[i],hits[i]);
		}
	}
}

void init_hits(int **hits,int Mx)
{
	int i;

	if (((*hits) = (int *) malloc(Mx*sizeof(int)))==0) {
			perror("malloc 4");exit(1);
	}
	
	for (i=0;i<Mx;i++) (*hits)[i]=0;
}

int get_type(int cP1,int cP2,int cP3,int iP1,int iP2,int iP3)
{
	int cT,iT;

	if (cP1==-1 && cP2==-1 && cP3==-1 && iP1==-1 && iP2==-1 && iP3==-1) return(APOS);

	cT=POS3;
	if (cP3==-1) cT--;
	if (cP2==-1) cT--;

	iT=POS3;
	if (iP3==-1) iT--;
	if (iP2==-1) iT--;

	if (iT != cT) {
		fprintf(stderr,"positions do not match (1)\n");exit(1);
	}

	if ((cP1==-1 && iP1!=-1) || (cP1!=-1 && iP1==-1)) {
		fprintf(stderr,"positions do not match (2)\n");exit(1);
	}

	if ((cP2==-1 && iP2!=-1) || (cP2!=-1 && iP2==-1)) {
		fprintf(stderr,"positions do not match (3)\n");exit(1);
	}

	if ((cP3==-1 && iP3!=-1) || (cP3!=-1 && iP3==-1)) {
		fprintf(stderr,"positions do not match (4)\n");exit(1);
	}

	return(cT);
}

void dump_data(unsigned char **data,char *fName,int cnt)
{
	int i;

	printf("FILE=%s\n",fName);
	for (i=0;i<cnt;i++) printf("%s\n",data[i]);
}

int maxPos(int p1,int p2,int p3)
{
	int m1,m2;
	m1=(p1>p2?p1:p2);
	m2=(m1>p3?m1:p3);
	return(m2);
}

int read_data(char *fNam,int MxCnt,int MxLgh,int MxPos,unsigned char ***data)
{
	FILE *fil;
	unsigned char lin[128],dummy;
	int i,cnt,lgh;

	if (((*data) = (unsigned char **) malloc(MxCnt*sizeof(unsigned char *)))==0) {
			perror("malloc 5");exit(1);
	}
	for (i=0;i<MxCnt;i++) {
		if (((*data)[i] = (unsigned char *) malloc(MxLgh+1))==0) {
			perror("malloc 6");exit(1);
		}
	}

	if ((fil=fopen(fNam,"r"))==0) {
		perror("open");exit(1);
	}

	cnt=0;
	while (fscanf(fil,"%[^\n]",lin)==1) {
		fscanf(fil,"%c",&dummy);
		if ((lgh=strlen(lin))<MxPos) {
			fprintf(stderr,"%s: %s (line too short)\n",fNam,lin);exit(1);
		}
		if (cLGH==0) cLGH=lgh;
		if (lgh != cLGH) {
			fprintf(stderr,"uneven length (%d)\n",cLGH);exit(1);
		}
		if (cnt>=MxCnt) {
			fprintf(stderr,"%s: reached max count\n",fNam);exit(1);
		}
		bcopy(lin,(*data)[cnt],lgh);
		(*data)[cnt][lgh]=0;
		//printf("lin=%s\n",lin);
		cnt++;
	}

	fclose(fil);
	return(cnt);
}

int get_line_count(char *fName)
{
	FILE *fil;
	char lin[1024];
	int cnt;

	sprintf(lin,"wc -l %s\n",fName);

	if ((fil=popen(lin,"r"))==0) {
		perror("popen");exit(1);
	}

	if (fscanf(fil,"%d",&cnt)!=1) {
	}
	pclose(fil);
	return(cnt);
}
