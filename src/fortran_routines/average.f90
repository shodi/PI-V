SUBROUTINE AVERAGE(ARR, SIZE)
    IMPLICIT NONE

    INTEGER:: SIZE, COUNT
    REAL:: SUM
    REAL, DIMENSION(SIZE):: ARR
    COUNT = 1
    SUM = 0
!f2py intent(in) size
!f2py intent(out) sum
!f2py depend(size) arr

100 IF (COUNT.LE.SIZE) THEN
        SUM = SUM + ARR(COUNT)
        COUNT = COUNT + 1
        GOTO 100
    ENDIF
    SUM = SUM / SIZE
    
END SUBROUTINE AVERAGE