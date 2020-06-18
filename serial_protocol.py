from opentrons import protocol_api

metadata = {'apiLevel': '2.2'}

def quick_mix(pipette, well, volume, rep=3,  rate = 8.0, adj_height = 6.0):
    """ Mix the solution up and down specified number of times
    rep = number of repetitions
    rate = the rate to aspirate and dispense while mixing
    adj_height = how far above the well bottom to dispense the fluid
    """
    old_height = pipette.well_bottom_clearance.dispense
    pipette.well_bottom_clearance.dispense = adj_height
    for i in range(rep):
        pipette.aspirate(20, well, rate=rate)
        pipette.dispense(20, well, rate=rate)
    pipette.well_bottom_clearance.dispense = old_height


def run(protocol:protocol_api.ProtocolContext):
    
    """
    Creates 2 tip racks,1x 15 mL reservoit, 1x 24 position tube, 1x 96 position
    
    Transfer 100 uL 
    """
    tip_20 = protocol.load_labware('opentrons_96_filtertiprack_20ul',1)
    tip_200 = protocol.load_labware('opentrons_96_filtertiprack_200ul',2)
    
    reservoir = protocol.load_labware('nest_12_reservoir_15ml', 3)
    
    block_24well = protocol.load_labware('opentrons_24_aluminumblock_nest_1.5ml_snapcap',4)
    block_96well = protocol.load_labware('opentrons_96_aluminumblock_generic_pcr_strip_200ul',5)

    p20 = protocol.load_instrument('p20_single_gen2', 'left', tip_racks = [tip_20])
    p300_multi = protocol.load_instrument('p300_multi_gen2', 'right', tip_racks = [tip_200])
    
    
    #Prepare to fill the PCR tubes, change the offset, and transfer liquid
    p300_multi.well_bottom_clearance.dispense = 3 # Raise the tip up slightly from the bottom
    p300_multi.well_bottom_clearance.aspirate = 3
    
    cols = [block_96well.columns_by_name()[well_id] for well_id in ['1','2']]
    p300_multi.distribute(20*2,reservoir.wells_by_name()['A1'], cols)

    
    #Fill the PCR tubes with samples (create the first sample, then serially dilute from that)
    p20.pick_up_tip()
    p20.transfer(20, block_24well.wells_by_name()['A1'], block_96well.wells_by_name()['A1'], new_tip='never')
    quick_mix(p20,block_96well.wells_by_name()['A1'],20,3,4.0 )
    p20.drop_tip()
    
    sample_wells = ['A1','B1','C1','D1','E1','F1','G1','H1']
    
    for from_well, to_well in zip(sample_wells[:-1],sample_wells[1:]):
        p20.pick_up_tip()
        p20.aspirate(20, block_96well.wells_by_name()[from_well], rate = 2.0)
        p20.dispense(20, block_96well.wells_by_name()[to_well], rate = 2.0 )
        quick_mix(p20,block_96well.wells_by_name()[to_well],20,3,5.0 )
        p20.drop_tip()
        
    return p300_multi
