mod = 1.5;        // Module (mm)
teeth = 10;       // Pinion teeth
pressure_angle = 20;
thickness = 5;    // Extrusion height (mm)
rack_teeth = 12;
rack_pos = $t; // [0:0.001:1]

pitch = PI * mod;
pitch_d = mod * teeth;
addendum = mod;
dedendum = 1.25 * mod;

module rack_tooth() {
    top_w = pitch * 0.35;
    bot_w = pitch * 0.5;
    linear_extrude(height = thickness, center = false) {
        polygon(points=[
        [-bot_w/2, -dedendum],
        [ bot_w/2, -dedendum],
        [ top_w/2,  addendum],
        [-top_w/2,  addendum]
        ]);
    }
}

module rack() {
    len = rack_teeth * pitch;
    union() {
        translate([0, -dedendum - 4, 0])
            cube([len, 4, thickness]);
        for (i = [0 : rack_teeth - 1]) {
            translate([(i + 0.5) * pitch, 0, 0])
                rack_tooth();
        }
    }
}

module pinion() {
    outer_r = pitch_d / 2 + addendum;
    root_r = pitch_d / 2 - dedendum;
    union() {
        cylinder(h = thickness, r = root_r, $fn = 64);
        for (i = [0 : teeth - 1]) {
            rotate([0, 0, i * (360 / teeth)])
                translate([0, pitch_d / 2, 0])
                    rack_tooth();
        }
    }
}

degrees_per_tooth = 360 / teeth;
degrees_per_rack = degrees_per_tooth * rack_teeth;

translate([-pitch - rack_teeth * pitch * rack_pos,0,0])
    rack();
translate([0, pitch_d / 2, 0])
    rotate([0,0,degrees_per_rack*-rack_pos])
        pinion();
