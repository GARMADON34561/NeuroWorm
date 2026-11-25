from neuroworm.brain.connectome import *

print("Testing AWA -> AIB -> AVA\n")

for i in range(20):

    print(f"Stimulus {i+1}")

    if AWA.stimulate():

        print("AWA FIRED")

        if AIB.stimulate(
            AWA_AIB.transmit()
        ):

            print("AIB FIRED")

            if AVA.stimulate(
                AIB_AVA.transmit()
            ):

                print("AVA FIRED")
                print("MOTOR OUTPUT")