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