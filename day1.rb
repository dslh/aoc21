#!/usr/bin/env ruby

depths = File.readlines('./input/1.txt').map(&:to_i)

puts 'Part 1:'
puts depths.each_cons(2).select { |a, b| a < b }.size

puts 'Part 2:'
puts depths.each_cons(3).each_cons(2).select { |a, b| a.sum < b.sum }.size
