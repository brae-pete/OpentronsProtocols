from opentrons import protocol_api

def quick_mix(pipette, well, volume, rep=3,  rate = 8.0, adj_height = 6.0, blow_out = True):
    """ Mix the solution up and down specified number of times
    rep = number of repetitions
    rate = the rate to aspirate and dispense while mixing
    adj_height = how far above the well bottom to dispense the fluid
    """
    old_height = pipette.well_bottom_clearance.dispense
    pipette.well_bottom_clearance.dispense = adj_height
    if not pipette.hw_pipette['has_tip']:
        pipette.pick_up_tip()
    for i in range(rep):
        pipette.aspirate(20, well, rate=rate)
        pipette.dispense(20, well, rate=rate)
 
    if blow_out:
        pipette.blow_out()
        
    pipette.touch_tip()
    pipette.well_bottom_clearance.dispense = old_height
    pipette.drop_tip()

metadata = {'apiLevel': '2.4',
           'protocolName':'NucleosomeAssemblyProtocol',
           'author':'Brae',
           'description':'Epimark Nucleosome Assembly Protocol'}


def run(protocol:protocol_api.ProtocolContext):
    
    """
    Epimark Nucleosome Assembly using the Dilution method for 50 pmol using their control DNA as a template. 
    """
    tip_20 = protocol.load_labware('opentrons_96_filtertiprack_20ul',1)
    tip_200 = protocol.load_labware('opentrons_96_filtertiprack_200ul',2)
    
    tubes = protocol.load_labware('opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', 3)
    
    p20 = protocol.load_instrument('p20_single_gen2', 'left', tip_racks = [tip_20])
    p300_multi = protocol.load_instrument('p300_multi_gen2', 'right', tip_racks = [tip_200])
    
    
    sample = tubes.wells()[0]
    dilution = tubes.wells()[1]
    
    steps = ['Step 4', 'Step 5', 'Step 6', 'Step 7']
    transfers = [7, 13, 27, 93]
    # Wait 30 min then add 7 uL of NaCl to 20 uL Reaction Mixture 
    for step_id, liquid in zip(steps, transfers):
        
        protocol.delay(minutes=0.1)
        p20.transfer(liquid, dilution, sample, touch_tip = True, blow_out = True, )
        quick_mix(p20, sample, 20, rep=25, rate=20, adj_height =6) # volume, speed, repetitions
    
    return p20
