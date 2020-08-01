
c****************************************************************************
c	This user element subroutine performs the following tasks:
c 	1- Read the Stiffness Matrix from a txt file and assign it to AMATRX of each user element 
c   2- Computes the RHS of each user element
c
c  
c
c****************************************************************************
    
       SUBROUTINE UEL (RHS, AMATRX, SVARS, ENERGY, NDOFEL, NRHS, NSVARS,
     & PROPS, NPROPS, COORDS, MCRD, NNODE, U, DU, V, A, JTYPE, TIME,
     & DTIME, KSTEP, KINC, JELEM, PARAMS, NDLOAD, JDLTYP, ADLMAG,
     & PREDEF, NPREDF, LFLAGS, MLVARX, DDLMAG, MDLOAD, PNEWDT, JPROPS,
     & NJPRO, PERIOD)
       INCLUDE 'ABA_PARAM.INC'	! c This statement has to be included in each subroutine
       DIMENSION RHS(MLVARX,*), AMATRX(NDOFEL,NDOFEL), PROPS(*),
     & SVARS(*), ENERGY(8), COORDS(MCRD, NNODE), U(NDOFEL),
     & DU(MLVARX,*), V(NDOFEL), A(NDOFEL), TIME(2), PARAMS(*),
     & JDLTYP(MDLOAD,*), ADLMAG(MDLOAD,*), DDLMAG(MDLOAD,*),
     & PREDEF(2, NPREDF, NNODE), LFLAGS(*), JPROPS(*)

        real(8)  Kij(8,8)!, AMATRX(8,8), RHS(8,1)   ! Declaration
	  integer counter, ilines, temp,i 
	  ! Initialize K matrix to zero
	  do i = 1, 8
          do j = 1, 8
               Kij(i,j)=0.d0
          end do
        end do
          
	  open(10, file="C:\Users\ga53quk\Desktop\Plate_with_hole\UEL_test\Run_3\counter.txt")	            ! set the path to the location where counter.txt is stored 
        read(10,*) counter
        close (10,status='delete')
        temp=counter+1
        open(10, file="C:\Users\ga53quk\Desktop\Plate_with_hole\UEL_test\Run_3\counter.txt",status='new')	! set the path to the location where counter.txt is stored
        write(10,*) temp
        close (10) 
        
        open(12, file ="C:\Users\ga53quk\Desktop\Plate_with_hole\UEL_test\Run_3\Stifness_matrix_Element.txt" )    ! set the path to the location where Stifness_matrix_Element.txt is stored
        
        if (counter==0) then     ! Reading Stifness_matrix_Element.txt from the beginning 
			read(12,*) ((Kij(i,j), j=1,8), i=1,8)
        else               ! Skipping 8 lines of Stifness_matrix_Element.txt 
          do ilines = (1),(8*counter)
              read(12,*) 
          end do
          
          read(12,*) ((Kij(i,j), j=1,8), i=1,8)   !Continutation of reading
        endif
      
        AMATRX = Kij       ! Assign AMATRX to Kij
        
        close(12)
        
        do i =1,8             ! Assign RHS to zeros
			RHS(i,1)=0.d0
        end do

        return
        end	
	