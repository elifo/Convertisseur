subroutine trapezoid (N,dt,vecteur,integral)

      INTEGER  :: N
      REAL*4, INTENT(IN) :: vecteur(N)
      REAL*4, INTENT(OUT):: integral(N)
!f2py depend(N) vecteur, integral
!f2py intent(out) integral

      REAL*4, INTENT(IN)                     :: dt
      REAL*4                                 :: vecprec, cumul
      INTEGER                                :: i 

      vecprec  = 0.0
      cumul    = 0.0
      
      do i = 1,N
        integral (i) = cumul+ dt* 0.5* (vecteur(i)+vecprec)
        vecprec      = vecteur(i)
        cumul        = integral(i)
      end do


end subroutine trapezoid