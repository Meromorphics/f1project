functions
{
    // equation 4 of Glickman and Hennessy
    // for a given race, the input t vector must be ordered according to race results
    real get_ln_likelihood(vector t)
    {
        int n = 20;
        real ln_likelihood = 0;
        for (i in 1:(n - 1))
        {
            ln_likelihood = ln_likelihood + t[i] - log_sum_exp(t[i:n]);
        }
        return ln_likelihood;
    }
}

data
{
    int<lower=0> n_drivers; // number of total drivers; not necessarily how many in participate in each race
    int<lower=0> n_constructors; // number of constructors
    int<lower=0> n_races; // number of races

    // for each race, the 20 (here 20, change all 20's in the code to however drivers take place in each race) drivers
    // are ordered 1, ..., 20. Each driver has a unique integer identifier (driver "1", driver "2", ..., driver "20").
    // For each race, assemble the finishing positions into a vector and put each driver's integer identifier in the place they scored.
    // For example, with 4 drivers 1, 2, 3, 4, if 3 wins, then 2, then 4, then 1, assemble the vector [3, 2, 4, 1]
    // driver_orderings is the concatenation of all of those vectors for each race in order of race
    array[20 * n_races] int<lower=1, upper=n_drivers> driver_orderings;
    // Same construction as drivers, but for constructors. Should have repeat constructor integer identifiers if a constructor
    // has more than 1 driver.
    array[20 * n_races] int<lower=1, upper=n_constructors> constructor_orderings;

    // I tried making the above two constructions out of matrices or 2d arrays, but I would get compilation errors
}

parameters
{
    vector[n_drivers] t_d; // driver skills, ordered by driver integer identifiers
    vector[n_constructors] t_c; // constructor skills, ordered by constructor integer identifiers
}

model
{
    // Prior declaration
    // Burkner: says BRMS package uses a half student t prior with 3 degrees of freedom as default 
    // doing a regular student t with 3 degrees of freedom for priors here
    t_d ~ student_t(3, 0, 1);
    t_c ~ student_t(3, 0, 1);

    // target: what STAN wants for the ln likelihood
    int n = 20;
    for (i in 1:n_races)
    {
        // get the driver and constructor orderings of the ith race
        array[n] int driver_ordering_i = segment(driver_orderings, 1+(i-1)*n, n);
        array[n] int constructor_orderings_i = segment(constructor_orderings, 1+(i-1)*n, n);
        // find the corresponding skills in order of placement
        vector[n] t_d_i = t_d[driver_ordering_i];
        vector[n] t_c_i = t_c[constructor_orderings_i];
        // get the ln likelihood
        // over n_races, so likelihoods multiply (independence); means adding for natural logarithm
        target += get_ln_likelihood(t_d_i + t_c_i);
    }

}

generated quantities
{
    // loo command wants a vector log_lik containing ln likelihoods of each race
    int n = 20;
    vector[n_races] log_lik;
    for (i in 1:n_races)
    {
        array[n] int driver_ordering_i = segment(driver_orderings, 1+(i-1)*n, n);
        array[n] int constructor_orderings_i = segment(constructor_orderings, 1+(i-1)*n, n);
        vector[n] t_d_i = t_d[driver_ordering_i];
        vector[n] t_c_i = t_c[constructor_orderings_i];

        log_lik[i] = get_ln_likelihood(t_d_i + t_c_i);
  }
}
