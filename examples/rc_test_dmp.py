if __name__ == "__main__":

    # This is only necessary if package has not been installed
    import sys
    sys.path.append('..')

# import python libraries
import time
import getopt

# import rc library
# This automatically initizalizes the robotics cape
import rc 
import rc.mpu9250 as mpu9250

def usage():
    print("""usage: python rc_test_dmp [options] ...
Options are:
-m          enable magnetometer
-s rate     Set sample rate in HZ (default 100)
            Sample rate must be a divisor of 200
-c          Show raw compass angle
-a          Print Accelerometer Data
-g          Print Gyro Data
-t          Print TaitBryan Angles
-q          Print Quaternion Vector
-o          Show a menu to select IMU orientation
-h          print this help message""")

def main():

    # exit if no options
    if len(sys.argv) < 2:
        usage()
        sys.exit(2)

    # Parse command line
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hmcagtqos:", ["help"])

    except getopt.GetoptError as err:
        # print help information and exit:
        print('rc_test_dmp: illegal option {}'.format(sys.argv[1:]))
        usage()
        sys.exit(2)

    # defaults
    enable_magnetometer = False
    show_compass = False
    show_gyro = False
    show_accel = False
    show_quat = False
    show_tb = False
    sample_rate = 100

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in "-s":
            sample_rate = int(a)
        elif o == "-m":
            enable_magnetometer = True
        elif o == "-c":
            show_compass = True
        elif o == "-a":
            show_accel = True
        elif o == "-g":
            show_gyro = True
        elif o == "-q":
            show_quat = True
        elif o == "-t":
            show_tb = True
        else:
            assert False, "Unhandled option"

    try:

        # set state to rc.RUNNING
        rc.set_state(rc.RUNNING)

        # magnetometer ?
        mpu9250.initialize(enable_dmp = True,
                           dmp_sample_rate = sample_rate,
                           enable_magnetometer = enable_magnetometer)
        
        # message
        print("Press Ctrl-C to exit")

        # header
        if show_accel:
            print("   Accel XYZ (m/s^2) |", end='')
        if show_gyro:
            print("    Gyro XYZ (deg/s) |", end='')
        if show_compass:
            print("     Mag Field XYZ (uT) |", end='')
            print("Head(rad)|", end='')
        if show_quat:
            print("                 Quaternion |", end='')
        if show_tb:
            print("    Tait Bryan (rad) |", end='')
        print(' Temp (C)')
        
        # keep running
        while rc.get_state() != rc.EXITING:

            # running
            if rc.get_state() == rc.RUNNING:
                
                data = mpu9250.read()
                temp = mpu9250.read_imu_temp()

                print('\r', end='')
                if show_accel:
                    print('{0[0]:6.2f} {0[1]:6.2f} {0[2]:6.2f} |'
                          .format(data['accel']), end='')
                if show_gyro:
                    print('{0[0]:6.1f} {0[1]:6.1f} {0[2]:6.1f} |'
                          .format(data['gyro']), end='')
                if show_compass:
                    print('{0[0]:7.1f} {0[1]:7.1f} {0[2]:7.1f} |'
                          .format(data['mag']), end='')
                    print('  {:6.2f} |'
                          .format(data['head']), end='')
                if show_quat:
                    print('{0[0]:6.1f} {0[1]:6.1f} {0[2]:6.1f} {0[3]:6.1f} |'
                          .format(data['quat']), end='')
                if show_tb:
                    print('{0[0]:6.2f} {0[1]:6.2f} {0[2]:6.2f} |'
                          .format(data['tb']), end='')
                print('   {:6.1f}'.format(temp), end='')
                        
                # no need to sleep

    except (KeyboardInterrupt, SystemExit):
        # handle what to do when Ctrl-C was pressed
        pass
        
    finally:

        # say bye
        print("\nInterrupted.")
            
# exiting program will automatically clean up cape

if __name__ == "__main__":
    main()
