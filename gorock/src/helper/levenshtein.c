
#include "levenshtein.h"

long levenshtein_distance(char *cpStr1, char *cpStr2)
{
    char *cpSmaller, *cpLargger;
    size_t *pPriv, *pCurr, *pTemp;
    size_t lSmallerSize, lLarggerSize, lDistance, lSubstitutions, lStr1Size, lStr2Size;

    lStr1Size = strlen( cpStr1 );
    lStr2Size = strlen( cpStr2 );

    if ( lStr1Size > lStr2Size )
    {
        cpLargger = cpStr1;
        cpSmaller = cpStr2;
        lLarggerSize = lStr1Size;
        lSmallerSize = lStr2Size;
    } else {
        cpLargger = cpStr2;
        cpSmaller = cpStr1;
        lLarggerSize = lStr2Size;
        lSmallerSize = lStr1Size;
    }

    if ( !(pPriv = (size_t *) malloc( (lSmallerSize + 1) * sizeof(size_t) )) )
        return -1;

    for (size_t i = 0; i <= lSmallerSize; i++)
        pPriv[i] = i;

    for (size_t lIdx1 = 0; lIdx1 < lLarggerSize; lIdx1++)
    {
        if ( !(pCurr = (size_t *) malloc( (lSmallerSize + 1) * sizeof(size_t) )) )
            return -1;

        memset(pCurr + 1, 0x00, lSmallerSize * sizeof(size_t));
        pCurr[0] = lIdx1 + 1;

        for (size_t lIdx2 = 0; lIdx2 < lSmallerSize; lIdx2++)
        {
            lDistance = pPriv[lIdx2 + 1] + 1;

            if ( lDistance > (pCurr[lIdx2] + 1) )
                lDistance = pCurr[lIdx2] + 1;

            lSubstitutions = pPriv[lIdx2] + ( cpLargger[lIdx1] != cpSmaller[lIdx2] );

            if ( lDistance > lSubstitutions )
                lDistance = lSubstitutions;

            pCurr[lIdx2 + 1] = lDistance;

        }

        pTemp = pPriv;
        pPriv = pCurr;

        free( pTemp );
    }

    lDistance = pPriv[lSmallerSize];
    free(pPriv);

    return lDistance;
}
