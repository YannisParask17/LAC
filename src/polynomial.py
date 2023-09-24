# Scale up the thickness
thickness_new = thickness * scaling_factor   # Scale up thickness
z_new = c2_def[:, 2] * scaling_factor         # Scale up the z direction
radius_new = radius * scaling_factor

# Fit a polynomial to the thickness
poly_coeffs = np.polyfit(radius_new, thickness_new, 8)
thickness_poly = np.polyval(poly_coeffs, radius_new)
r2 = r2_score(thickness_new, thickness_poly)

np.savetxt(polynomial_path, poly_coeffs)
